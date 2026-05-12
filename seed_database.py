from datetime import datetime, timedelta

from sqlmodel import Session, select, delete

from database import engine
from models_a import Genre, Movie
from models_b import Hall, HallType, Screening, Seat, SeatType
from models_c import Reservation, User


TARGET_ROW_COUNT = 10


GENRE_SEED_DATA = [
	("Action", "Brzi i dinamični filmovi", 9.2, True),
	("Drama", "Emotivne i životne priče", 8.6, True),
	("Sci-Fi", "Naučna fantastika i futurizam", 8.8, True),
	("Crime", "Kriminalističke i triler priče", 9.0, True),
	("Animation", "Animirani filmovi za sve uzraste", 8.3, True),
	("Comedy", "Komedije za opuštanje", 7.9, True),
	("Horror", "Horor i psihološki trileri", 7.4, True),
	("Romance", "Romantične priče", 7.2, True),
	("Adventure", "Avanture i putovanja", 8.1, True),
	("Documentary", "Dokumentarni filmovi", 6.8, True),
]


MOVIE_SEED_DATA = [
	("The Dark Knight", "Christopher Nolan", 152, 2008, 9.0, True, "Crime"),
	("Inception", "Christopher Nolan", 148, 2010, 8.8, True, "Sci-Fi"),
	("Interstellar", "Christopher Nolan", 169, 2014, 8.6, True, "Sci-Fi"),
	("The Shawshank Redemption", "Frank Darabont", 142, 1994, 9.3, False, "Drama"),
	("Forrest Gump", "Robert Zemeckis", 142, 1994, 8.8, False, "Drama"),
	("Mad Max: Fury Road", "George Miller", 120, 2015, 8.1, True, "Action"),
	("John Wick", "Chad Stahelski", 101, 2014, 7.4, True, "Action"),
	("Top Gun: Maverick", "Joseph Kosinski", 130, 2022, 8.3, True, "Adventure"),
	("Pulp Fiction", "Quentin Tarantino", 154, 1994, 8.9, False, "Crime"),
	("The Lion King", "Roger Allers", 88, 1994, 8.5, False, "Animation"),
]


SEAT_TYPE_SEED_DATA = [
	"VIP",
	"Standard",
	"Economy",
	"Premium",
	"Couple",
	"Accessible",
	"Front Row",
	"Balcony",
	"Box",
	"Kids",
]


HALL_TYPE_SEED_DATA = [
	"Standard Hall",
	"IMAX Hall",
	"VIP Hall",
	"3D Hall",
	"Dolby Hall",
	"Small Hall",
	"Large Hall",
	"Private Hall",
	"Open Air Hall",
	"Kids Hall",
]


USER_SEED_DATA = [
	("Amar", "Hodzic", "amar1@example.com", 21, "+38761111111"),
	("Lejla", "Basic", "lejla2@example.com", 24, "+38762222222"),
	("Marko", "Ilic", "marko3@example.com", 29, "+38763333333"),
	("Amina", "Kadic", "amina4@example.com", 31, "+38764444444"),
	("Nedim", "Salihovic", "nedim5@example.com", 27, "+38765555555"),
	("Selma", "Hasic", "selma6@example.com", 33, "+38766666666"),
	("Tarik", "Dizdar", "tarik7@example.com", 26, "+38767777777"),
	("Maja", "Dodik", "maja8@example.com", 22, "+38768888888"),
	("Haris", "Mujic", "haris9@example.com", 28, "+38769999999"),
	("Ema", "Vukovic", "ema10@example.com", 25, "+387610101010"),
]


def _seed_genres(session: Session) -> list[Genre]:
	existing_names = {genre.name for genre in session.exec(select(Genre)).all()}
	genres = [
		Genre(name=name, description=description, popularity_score=score, movie_count=0, is_active=is_active)
		for name, description, score, is_active in GENRE_SEED_DATA
		if name not in existing_names
	]
	session.add_all(genres)
	session.commit()
	all_genres = session.exec(select(Genre)).all()
	for genre in all_genres:
		session.refresh(genre)
	return all_genres


def _seed_movies(session: Session, genres: list[Genre]) -> list[Movie]:
	genre_by_name = {genre.name: genre for genre in genres}
	existing_titles = {movie.title for movie in session.exec(select(Movie)).all()}
	movies = [
		Movie(
			title=title,
			director=director,
			duration_minutes=duration_minutes,
			release_year=release_year,
			rating=rating,
			trailer_url=None,
			is_currently_showing=is_currently_showing,
			genre_id=genre_by_name[genre_name].id,
		)
		for title, director, duration_minutes, release_year, rating, is_currently_showing, genre_name in MOVIE_SEED_DATA
		if title not in existing_titles
	]
	session.add_all(movies)
	session.commit()
	all_movies = session.exec(select(Movie)).all()
	for movie in all_movies:
		session.refresh(movie)
	return all_movies


def _sync_genre_movie_counts(session: Session, genres: list[Genre]) -> None:
	for genre in genres:
		genre.movie_count = len(session.exec(select(Movie).where(Movie.genre_id == genre.id)).all())
		session.add(genre)
	session.commit()


def _seed_seat_types(session: Session) -> list[SeatType]:
	existing_names = {seat_type.type_name for seat_type in session.exec(select(SeatType)).all()}
	seat_types = [SeatType(type_name=name) for name in SEAT_TYPE_SEED_DATA if name not in existing_names]
	session.add_all(seat_types)
	session.commit()
	all_seat_types = session.exec(select(SeatType)).all()
	for seat_type in all_seat_types:
		session.refresh(seat_type)
	return all_seat_types


def _seed_hall_types(session: Session) -> list[HallType]:
	existing_names = {hall_type.type_name for hall_type in session.exec(select(HallType)).all()}
	hall_types = [HallType(type_name=name) for name in HALL_TYPE_SEED_DATA if name not in existing_names]
	session.add_all(hall_types)
	session.commit()
	all_hall_types = session.exec(select(HallType)).all()
	for hall_type in all_hall_types:
		session.refresh(hall_type)
	return all_hall_types


def _seed_halls(session: Session, hall_types: list[HallType]) -> list[Hall]:
	existing_count = len(session.exec(select(Hall)).all())
	halls = [Hall(type_id=hall_types[index].id) for index in range(existing_count, TARGET_ROW_COUNT)]
	session.add_all(halls)
	session.commit()
	all_halls = session.exec(select(Hall)).all()
	for hall in all_halls:
		session.refresh(hall)
	return all_halls


def _seed_seats(session: Session, seat_types: list[SeatType], halls: list[Hall]) -> list[Seat]:
	existing_count = len(session.exec(select(Seat)).all())
	seats = [
		Seat(type_id=seat_types[index].id, hall_id=halls[index].id)
		for index in range(existing_count, TARGET_ROW_COUNT)
	]
	session.add_all(seats)
	session.commit()
	all_seats = session.exec(select(Seat)).all()
	for seat in all_seats:
		session.refresh(seat)
	return all_seats


def _seed_screenings(session: Session, halls: list[Hall], movies: list[Movie]) -> list[Screening]:
	base_start = datetime(2026, 5, 12, 12, 0)
	existing_count = len(session.exec(select(Screening)).all())
	screenings = []
	for index in range(existing_count, TARGET_ROW_COUNT):
		start_time = base_start + timedelta(hours=index * 2)
		end_time = start_time + timedelta(hours=2)
		screenings.append(
			Screening(
				start_time=start_time,
				end_time=end_time,
				has_break=index % 2 == 0,
				base_ticket_price=10.0 + index,
				hall_id=halls[index].id,
				movie_id=movies[index].id,
			)
		)
	session.add_all(screenings)
	session.commit()
	all_screenings = session.exec(select(Screening)).all()
	for screening in all_screenings:
		session.refresh(screening)
	return all_screenings


def _seed_users(session: Session) -> list[User]:
	existing_emails = {user.email for user in session.exec(select(User)).all()}
	users = [
		User(first_name=first_name, last_name=last_name, email=email, age=age, phone_number=phone_number, is_active=True)
		for first_name, last_name, email, age, phone_number in USER_SEED_DATA
		if email not in existing_emails
	]
	session.add_all(users)
	session.commit()
	all_users = session.exec(select(User)).all()
	for user in all_users:
		session.refresh(user)
	return all_users


def _seed_reservations(session: Session, users: list[User], screenings: list[Screening], seats: list[Seat]) -> list[Reservation]:
	existing_count = len(session.exec(select(Reservation)).all())
	reservations = [
		Reservation(user_id=users[index].id, screening_id=screenings[index].id, seat_id=seats[index].id, price=10.0 + index, confirmed=index % 2 == 0)
		for index in range(existing_count, TARGET_ROW_COUNT)
	]
	session.add_all(reservations)
	session.commit()
	all_reservations = session.exec(select(Reservation)).all()
	for reservation in all_reservations:
		session.refresh(reservation)
	return all_reservations


def _reset_seed_tables(session: Session) -> None:
	for model in [Reservation, Screening, Seat, Hall, HallType, SeatType, Movie, Genre, User]:
		session.exec(delete(model))
	session.commit()


def seed_all_tables() -> None:
	with Session(engine) as session:
		_reset_seed_tables(session)
		genres = _seed_genres(session)
		movies = _seed_movies(session, genres)
		_sync_genre_movie_counts(session, genres)
		seat_types = _seed_seat_types(session)
		hall_types = _seed_hall_types(session)
		halls = _seed_halls(session, hall_types)
		seats = _seed_seats(session, seat_types, halls)
		screenings = _seed_screenings(session, halls, movies)
		users = _seed_users(session)
		_seed_reservations(session, users, screenings, seats)