from datetime import datetime
from sqlalchemy.orm import Session
from models.attendance import Attendance
from models.attendance_event import AttendanceEvent


class AttendanceService:

    @staticmethod
    def get_open_session(db: Session, user_id: int):
        return db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_out.is_(None)
        ).order_by(Attendance.id.desc()).first()


    @staticmethod
    def close_open_events(db: Session, attendance: Attendance):
        last_event = db.query(AttendanceEvent).filter(
            AttendanceEvent.attendance_id == attendance.id
        ).order_by(AttendanceEvent.id.desc()).first()

        if not last_event:
            return

        if last_event.event_type == "BREAK_START":
            db.add(AttendanceEvent(
                attendance_id=attendance.id,
                event_type="BREAK_END"
            ))

        elif last_event.event_type == "IDLE_START":
            db.add(AttendanceEvent(
                attendance_id=attendance.id,
                event_type="IDLE_END"
            ))


    @staticmethod
    def login(db: Session, user_id: int):
        # close previous session if exists
        open_session = AttendanceService.get_open_session(db, user_id)

        if open_session:
            AttendanceService.close_open_events(db, open_session)
            open_session.check_out = datetime.utcnow()
            open_session.status = "LOGGED_OUT"

        # create new session
        new_session = Attendance(
            user_id=user_id,
            status="WORKING"
        )

        db.add(new_session)
        db.commit()
        db.refresh(new_session)

        return new_session


    @staticmethod
    def break_start(db: Session, user_id: int):
        session = AttendanceService.get_open_session(db, user_id)

        if not session or session.status != "WORKING":
            raise Exception("Invalid state for break start")

        db.add(AttendanceEvent(
            attendance_id=session.id,
            event_type="BREAK_START"
        ))

        session.status = "BREAK"
        db.commit()


    @staticmethod
    def break_end(db: Session, user_id: int):
        session = AttendanceService.get_open_session(db, user_id)

        db.add(AttendanceEvent(
            attendance_id=session.id,
            event_type="BREAK_END"
        ))

        session.status = "WORKING"
        db.commit()


    @staticmethod
    def idle_start(db: Session, user_id: int):
        session = AttendanceService.get_open_session(db, user_id)

        if not session or session.status != "WORKING":
            return

        db.add(AttendanceEvent(
            attendance_id=session.id,
            event_type="IDLE_START"
        ))

        session.status = "IDLE"
        db.commit()


    @staticmethod
    def logout(db: Session, user_id: int):
        session = AttendanceService.get_open_session(db, user_id)

        if not session:
            return

        AttendanceService.close_open_events(db, session)

        session.check_out = datetime.utcnow()
        session.status = "LOGGED_OUT"

        db.commit()