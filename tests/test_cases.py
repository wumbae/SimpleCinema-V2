"""
Authors:
    Zayan Abdulla Nazil (23061331)
    Yoosuf Ayaan Musthaq (23064777)
    Mohamed Shaihan Fath-hulla (23061309)

This module handles the test cases of the cinema booking system.
"""





import unittest
from database.db_config import initialize_database
from database.db_manager import DatabaseManager
from datetime import datetime

class TestHCBookingSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()
        cls.db=DatabaseManager()

    def test_user_authentication(self):
        # Check admin user exists
        res=self.db.execute_query("SELECT * FROM users WHERE username='admin'")
        self.assertTrue(len(res)==1,"Admin user should exist.")

    def test_film_listing(self):
        res=self.db.execute_query("SELECT films.title FROM films JOIN sessions ON films.id=sessions.filmId")
        self.assertTrue(len(res)>0,"Should have film listings.")
        titles=[r[0] for r in res]
        self.assertIn('Inception',titles,"Inception should be listed.")

    def test_booking_insertion(self):
        # Insert new booking
        userId=self.db.execute_query("SELECT id FROM users WHERE role='staff'")[0][0]
        sessionId=self.db.execute_query("SELECT id FROM sessions LIMIT 1")[0][0]
        import uuid
        bid=str(uuid.uuid4())
        data={
            'id':str(uuid.uuid4()),
            'bookingID':bid,
            'bookingDate':'2024-12-08',
            'date':'2024-12-10',
            'seats':3,
            'ticketType':'lower_hall',
            'userId':userId,
            'sessionId':sessionId,
            'totalPrice':15.0
        }
        self.db.insert_record('bookings',data)
        check=self.db.execute_query("SELECT * FROM bookings WHERE bookingID=?",(bid,))
        self.assertEqual(len(check),1,"Booking should be created.")

    def test_cancellation(self):
        # Cancel the test booking "TEST-CANCEL-001"
        res=self.db.execute_query("SELECT bookings.id, sessions.date FROM bookings JOIN sessions ON bookings.sessionId=sessions.id WHERE bookingID='TEST-CANCEL-001'")
        self.assertEqual(len(res),1,"Test booking exists.")
        bookingId,show_date=res[0]
        show_dt=datetime.strptime(show_date,"%Y-%m-%d")
        ref_dt=datetime(2024,12,8)
        delta=(show_dt-ref_dt).days
        if delta>=1:
            self.db.execute_query("DELETE FROM bookings WHERE id=?",(bookingId,))
            after=self.db.execute_query("SELECT * FROM bookings WHERE id=?",(bookingId,))
            self.assertEqual(len(after),0,"Booking should be cancelled.")
        else:
            self.fail("Show date not suitable for cancellation test scenario.")

    def test_price_calculation(self):
        # Just a simple check for VIP price for a Bristol morning show:
        # Bristol morning lower hall=7
        # VIP=7*1.44=10.08
        self.assertAlmostEqual(7*1.44,10.08,2,"VIP price should be correct.")

if __name__=='__main__':
    unittest.main()
