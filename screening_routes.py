from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional
from database import get_session
from models_a import Movie
from models_b import Hall, HallType, Screening, ScreeningCreate, ScreeningHallRead, ScreeningMovieRead, ScreeningRead, ScreeningUpdate

router = APIRouter(prefix="/screenings", tags=["Screenings"])


def _normalize_datetime(value):
	if value.tzinfo is None:
		return value
	return value.replace(tzinfo=None)


def _screening_overlaps(
	session: Session,
	hall_id: int,
	start_time,
	end_time,
	exclude_screening_id: Optional[int] = None,
) -> bool:
	statement = select(Screening).where(Screening.hall_id == hall_id)
	if exclude_screening_id is not None:
		statement = statement.where(Screening.id != exclude_screening_id)

	normalized_start_time = _normalize_datetime(start_time)
	normalized_end_time = _normalize_datetime(end_time)

	for existing_screening in session.exec(statement).all():
		normalized_existing_start = _normalize_datetime(existing_screening.start_time)
		normalized_existing_end = _normalize_datetime(existing_screening.end_time)
		if normalized_start_time < normalized_existing_end and normalized_end_time > normalized_existing_start:
			return True
	return False


@router.get("movie-screenings-counter/{movie_id}", response_model=int)
def get_screenings_for_movie(movie_id: int, session: Session = Depends(get_session)):
	statement = select(Screening).where(Screening.movie_id == movie_id)
	return session.exec(statement).all().__len__()

@router.get("", response_model=list[Screening])
def get_screenings(
	hall_id: Optional[int] = Query(default=None, description="Filter by hall id"),
	movie_id: Optional[int] = Query(default=None, description="Filter by movie id"),
	session: Session = Depends(get_session)
):
	statement = select(Screening)
	if hall_id is not None:
		statement = statement.where(Screening.hall_id == hall_id)
	if movie_id is not None:
		statement = statement.where(Screening.movie_id == movie_id)
	return session.exec(statement).all()


@router.get("/with-details", response_model=list[ScreeningRead])
def get_screenings_with_details(
	hall_id: Optional[int] = Query(default=None, description="Filter by hall id"),
	movie_id: Optional[int] = Query(default=None, description="Filter by movie id"),
	session: Session = Depends(get_session)
):
	statement = select(Screening, Hall, HallType, Movie).join(Hall, Screening.hall_id == Hall.id).join(HallType, Hall.type_id == HallType.id).join(Movie, Screening.movie_id == Movie.id)
	if hall_id is not None:
		statement = statement.where(Screening.hall_id == hall_id)
	if movie_id is not None:
		statement = statement.where(Screening.movie_id == movie_id)
	rows = session.exec(statement).all()
	return [
		ScreeningRead(
			id=screening.id,
			start_time=screening.start_time,
			end_time=screening.end_time,
			has_break=screening.has_break,
			base_ticket_price=screening.base_ticket_price,
			hall=ScreeningHallRead(id=hall.id, type_id=hall.type_id, type_name=hall_type.type_name),
			movie=ScreeningMovieRead(
				id=movie.id,
				title=movie.title,
				director=movie.director,
				duration_minutes=movie.duration_minutes,
				release_year=movie.release_year,
				rating=movie.rating,
				trailer_url=movie.trailer_url,
				is_currently_showing=movie.is_currently_showing,
				genre_id=movie.genre_id,
			),
		)
		for screening, hall, hall_type, movie in rows
	]


@router.get("/{screening_id}", response_model=Screening)
def get_screening(screening_id: int, session: Session = Depends(get_session)):
	screening = session.get(Screening, screening_id)
	if not screening:
		raise HTTPException(status_code=404, detail="Projekcija nije pronadjena")
	return screening


@router.get("/{screening_id}/with-details", response_model=ScreeningRead)
def get_screening_with_details(screening_id: int, session: Session = Depends(get_session)):
	statement = select(Screening, Hall, HallType, Movie).join(Hall, Screening.hall_id == Hall.id).join(HallType, Hall.type_id == HallType.id).join(Movie, Screening.movie_id == Movie.id).where(Screening.id == screening_id)
	row = session.exec(statement).first()
	if not row:
		raise HTTPException(status_code=404, detail="Projekcija nije pronadjena")
	screening, hall, hall_type, movie = row
	return ScreeningRead(
		id=screening.id,
		start_time=screening.start_time,
		end_time=screening.end_time,
		has_break=screening.has_break,
		base_ticket_price=screening.base_ticket_price,
		hall=ScreeningHallRead(id=hall.id, type_id=hall.type_id, type_name=hall_type.type_name),
		movie=ScreeningMovieRead(
			id=movie.id,
			title=movie.title,
			director=movie.director,
			duration_minutes=movie.duration_minutes,
			release_year=movie.release_year,
			rating=movie.rating,
			trailer_url=movie.trailer_url,
			is_currently_showing=movie.is_currently_showing,
			genre_id=movie.genre_id,
		),
	)


@router.post("", response_model=Screening, status_code=201)
def create_screening(screening_in: ScreeningCreate, session: Session = Depends(get_session)):
	hall = session.get(Hall, screening_in.hall_id)
	if not hall:
		raise HTTPException(status_code=404, detail="Hall nije pronadjen")

	movie = session.get(Movie, screening_in.movie_id)
	if not movie:
		raise HTTPException(status_code=404, detail="Film nije pronadjen")

	if _screening_overlaps(session, screening_in.hall_id, screening_in.start_time, screening_in.end_time):
		raise HTTPException(status_code=409, detail="U toj sali vec postoji projekcija u tom terminu")

	db_screening = Screening.model_validate(screening_in)
	session.add(db_screening)
	session.commit()
	session.refresh(db_screening)
	return db_screening


@router.put("/{screening_id}", response_model=Screening)
def put_screening(screening_id: int, screening_in: ScreeningCreate, session: Session = Depends(get_session)):
	db_screening = session.get(Screening, screening_id)
	if not db_screening:
		raise HTTPException(status_code=404, detail="Projekcija nije pronadjena")

	hall = session.get(Hall, screening_in.hall_id)
	if not hall:
		raise HTTPException(status_code=404, detail="Hall nije pronadjen")

	movie = session.get(Movie, screening_in.movie_id)
	if not movie:
		raise HTTPException(status_code=404, detail="Film nije pronadjen")

	if _screening_overlaps(session, screening_in.hall_id, screening_in.start_time, screening_in.end_time, exclude_screening_id=screening_id):
		raise HTTPException(status_code=409, detail="U toj sali vec postoji projekcija u tom terminu")

	data = screening_in.model_dump()
	for key, value in data.items():
		setattr(db_screening, key, value)

	session.add(db_screening)
	session.commit()
	session.refresh(db_screening)
	return db_screening


@router.patch("/{screening_id}", response_model=Screening)
def patch_screening(screening_id: int, screening_in: ScreeningUpdate, session: Session = Depends(get_session)):
	db_screening = session.get(Screening, screening_id)
	if not db_screening:
		raise HTTPException(status_code=404, detail="Projekcija nije pronadjena")

	data = screening_in.model_dump(exclude_unset=True, exclude_none=True)  # <-- dodano exclude_none=True

	if "hall_id" in data:
		hall = session.get(Hall, data["hall_id"])
		if not hall:
			raise HTTPException(status_code=404, detail="Hall nije pronadjen")

	if "movie_id" in data:
		movie = session.get(Movie, data["movie_id"])
		if not movie:
			raise HTTPException(status_code=404, detail="Film nije pronadjen")

	new_hall_id = data.get("hall_id", db_screening.hall_id)
	new_start_time = data.get("start_time", db_screening.start_time)
	new_end_time = data.get("end_time", db_screening.end_time)
	if _screening_overlaps(session, new_hall_id, new_start_time, new_end_time, exclude_screening_id=screening_id):
		raise HTTPException(status_code=409, detail="U toj sali vec postoji projekcija u tom terminu")

	for key, value in data.items():
		if (key == "start_time" and value is not None) or (key == "end_time" and value is not None):
			value = _normalize_datetime(value)
			setattr(db_screening, key, value)
		else:
			setattr(db_screening, key, value)
	session.add(db_screening)
	session.commit()
	session.refresh(db_screening)
	return db_screening


@router.delete("/{screening_id}", status_code=204)
def delete_screening(screening_id: int, session: Session = Depends(get_session)):
	db_screening = session.get(Screening, screening_id)
	if not db_screening:
		raise HTTPException(status_code=404, detail="Projekcija nije pronadjena")

	session.delete(db_screening)
	session.commit()
