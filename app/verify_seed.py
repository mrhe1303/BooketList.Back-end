"""
Verification Test Script
Run this after seeding the database to verify everything works correctly
Usage: python verify_seed.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database import db
from app.models.user import User
from app.models.book import Book
from app.models.rating import Rating
from app.models.user_library import UserLibrary
from app.models.admin import Admin
from sqlalchemy import func

app = create_app()

def test_no_overlap():
    """Test 1: Verify no books appear in both UserLibrary and Rating for same user"""
    print("\n🧪 Test 1: Checking for overlap between UserLibrary and Rating...")
    
    with app.app_context():
        users = User.query.all()
        total_overlaps = 0
        
        for user in users:
            library_books = {ul.id_libro for ul in UserLibrary.query.filter_by(id_usuario=user.id_usuario).all()}
            rated_books = {r.id_libro for r in Rating.query.filter_by(id_usuario=user.id_usuario).all()}
            overlap = library_books & rated_books
            
            if overlap:
                print(f"   ❌ User {user.nombre_usuario}: {len(overlap)} overlapping books!")
                total_overlaps += len(overlap)
        
        if total_overlaps == 0:
            print("   ✅ PASSED: No overlap detected!")
            return True
        else:
            print(f"   ❌ FAILED: {total_overlaps} total overlapping books found")
            return False

def test_nullable_ratings():
    """Test 2: Verify some ratings have null calificacion values"""
    print("\n🧪 Test 2: Checking nullable ratings...")
    
    with app.app_context():
        total_ratings = Rating.query.count()
        null_ratings = Rating.query.filter(Rating.calificacion == None).count()
        
        if null_ratings > 0:
            percentage = (null_ratings / total_ratings) * 100
            print(f"   ✅ PASSED: {null_ratings}/{total_ratings} ratings without stars ({percentage:.1f}%)")
            return True
        else:
            print(f"   ❌ FAILED: All {total_ratings} ratings have star values (should have some nulls)")
            return False

def test_valid_states():
    """Test 3: Verify only valid estados in UserLibrary"""
    print("\n🧪 Test 3: Checking valid reading states in UserLibrary...")
    
    with app.app_context():
        valid_states = ['quiero_leer', 'leyendo']
        invalid_entries = UserLibrary.query.filter(
            ~UserLibrary.estado_lectura.in_(valid_states)
        ).all()
        
        if not invalid_entries:
            print("   ✅ PASSED: All UserLibrary entries have valid estados")
            return True
        else:
            print(f"   ❌ FAILED: Found {len(invalid_entries)} entries with invalid estados:")
            for entry in invalid_entries[:5]:  # Show first 5
                print(f"      - estado: '{entry.estado_lectura}'")
            return False

def test_data_counts():
    """Test 4: Verify expected data counts"""
    print("\n🧪 Test 4: Checking data counts...")
    
    with app.app_context():
        admin_count = Admin.query.count()
        user_count = User.query.count()
        book_count = Book.query.count()
        rating_count = Rating.query.count()
        library_count = UserLibrary.query.count()
        
        print(f"   Admins: {admin_count}")
        print(f"   Users: {user_count}")
        print(f"   Books: {book_count}")
        print(f"   Ratings (leídos): {rating_count}")
        print(f"   Library items (quiero_leer/leyendo): {library_count}")
        
        # Expected: 1 admin, 5 users, 112 books
        if admin_count == 1 and user_count == 5 and book_count == 111:
            print("   ✅ PASSED: Core counts look correct")
            return True
        else:
            print("   ⚠️  WARNING: Counts don't match expected values")
            print("      Expected: 1 admin, 5 users, 111 books")
            return False

def test_genre_distribution():
    """Test 5: Verify genre distribution"""
    print("\n🧪 Test 5: Checking genre distribution...")
    
    with app.app_context():
        genre_counts = db.session.query(
            Book.genero_libro,
            func.count(Book.id_libros)
        ).group_by(Book.genero_libro).all()
        
        expected = {
            'Clásicos': 20,
            'No-Ficción': 20,
            'Ciencia Ficción': 20,
            'Ficción': 17,
            'Latinoamericano': 20,
            'Historia': 14
        }
        
        print("   Genre Distribution:")
        all_correct = True
        for genero, count in genre_counts:
            expected_count = expected.get(genero, '?')
            status = "✓" if count == expected_count else "✗"
            print(f"      {status} {genero}: {count} books (expected: {expected_count})")
            if count != expected_count:
                all_correct = False
        
        if all_correct:
            print("   ✅ PASSED: Genre distribution matches expected")
            return True
        else:
            print("   ⚠️  WARNING: Some genre counts don't match")
            return False

def test_user_book_distribution():
    """Test 6: Verify each user has reasonable book counts"""
    print("\n🧪 Test 6: Checking user book distribution...")
    
    with app.app_context():
        users = User.query.all()
        all_good = True
        
        for user in users:
            library_count = UserLibrary.query.filter_by(id_usuario=user.id_usuario).count()
            rated_count = Rating.query.filter_by(id_usuario=user.id_usuario).count()
            total = library_count + rated_count
            
            # Expected: 10-15 in library, 8+ in ratings
            if 10 <= library_count <= 15 and rated_count >= 8:
                status = "✓"
            else:
                status = "✗"
                all_good = False
            
            print(f"   {status} {user.nombre_usuario}: {library_count} in library, {rated_count} read (total: {total})")
        
        if all_good:
            print("   ✅ PASSED: All users have reasonable book distributions")
            return True
        else:
            print("   ⚠️  WARNING: Some users have unusual distributions")
            return False

def run_all_tests():
    """Run all verification tests"""
    print("=" * 60)
    print("🔍 RUNNING SEED VERIFICATION TESTS")
    print("=" * 60)
    
    tests = [
        test_no_overlap,
        test_nullable_ratings,
        test_valid_states,
        test_data_counts,
        test_genre_distribution,
        test_user_book_distribution
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your seed is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review the output above.")
    
    print("=" * 60)

if __name__ == '__main__':
    run_all_tests()
