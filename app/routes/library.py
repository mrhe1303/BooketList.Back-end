from flask import Blueprint, request, jsonify
from app.models import UserLibrary, Book
from app import db
from app.errors import bad_request, not_found, internal_error
from flask_jwt_extended import jwt_required, get_jwt_identity

library_bp = Blueprint('library', __name__)

@library_bp.route('/my-library', methods=['GET'])
@jwt_required()
def get_my_library():
    """
    Obtener la librería personal del usuario actual
    """
    try:
        user_id = get_jwt_identity()
        
        # Obtener libros en la librería del usuario
        user_library = UserLibrary.query.filter_by(id_usuario=user_id).all()
        
        library_books = []
        for item in user_library:
            book = Book.query.get(item.id_libro)
            if book:
                library_books.append({
                    'library_id': item.id_biblioteca,
                    'book': book.serialize(),
                    'reading_state': item.estado_lectura,
                    'added_at': item.created_at.isoformat() if item.created_at else None
                })
        
        return jsonify({
            'user_id': user_id,
            'total_books': len(library_books),
            'books': library_books
        }), 200
    
    except Exception as e:
        return internal_error(str(e))

@library_bp.route('/my-library/books', methods=['POST'])
@jwt_required()
def add_book_to_my_library():
    """
    Agregar libro a la librería personal del usuario
    Acepta: id_libro, estado_lectura (opcional, default: 'quiero_leer')
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('id_libro'):
            return bad_request('ID del libro es requerido')
        
        book_id = data['id_libro']
        reading_state = data.get('estado_lectura', 'quiero_leer')
        
        # Validar estado de lectura
        valid_states = ['quiero_leer', 'leyendo', 'leido']
        if reading_state not in valid_states:
            return bad_request(f'Estado de lectura inválido. Debe ser: {", ".join(valid_states)}')
        
        # Verificar si el libro existe
        book = Book.query.get(book_id)
        if not book:
            return not_found('Libro no encontrado')
        
        # Verificar si ya está en la librería
        existing = UserLibrary.query.filter_by(
            id_usuario=user_id, 
            id_libro=book_id
        ).first()
        
        if existing:
            return bad_request('El libro ya está en tu librería')
        
        # Agregar a la librería
        library_item = UserLibrary(
            id_usuario=user_id,
            id_libro=book_id,
            estado_lectura=reading_state
        )
        
        db.session.add(library_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Libro agregado a tu librería personal exitosamente',
            'book': book.serialize(),
            'reading_state': reading_state
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book_in_library(book_id):
    """
    Actualizar estado de lectura de un libro en la librería
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Buscar el item en la librería
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if not library_item:
            return not_found('Libro no encontrado en tu librería personal')
        
        # Actualizar estado de lectura si se proporciona
        if 'estado_lectura' in data:
            valid_states = ['quiero_leer', 'leyendo', 'leido']
            if data['estado_lectura'] not in valid_states:
                return bad_request(f'Estado de lectura inválido. Debe ser: {", ".join(valid_states)}')
            library_item.estado_lectura = data['estado_lectura']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Libro actualizado exitosamente',
            'library_item': library_item.serialize()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book_from_my_library(book_id):
    """
    Remover libro de la librería personal del usuario
    """
    try:
        user_id = get_jwt_identity()
        
        # Buscar el item en la librería
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        if not library_item:
            return not_found('Libro no encontrado en tu librería personal')
        
        db.session.delete(library_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Libro removido de tu librería personal exitosamente'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return internal_error(str(e))

@library_bp.route('/my-library/books/<int:book_id>', methods=['GET'])
@jwt_required()
def check_book_in_my_library(book_id):
    """
    Verificar si un libro está en la librería personal del usuario
    """
    try:
        user_id = get_jwt_identity()
        
        library_item = UserLibrary.query.filter_by(
            id_usuario=user_id,
            id_libro=book_id
        ).first()
        
        book = Book.query.get(book_id)
        
        response = {
            'in_my_library': library_item is not None,
            'book': book.serialize() if book else None
        }
        
        if library_item:
            response['reading_state'] = library_item.estado_lectura
        
        return jsonify(response), 200
    
    except Exception as e:
        return internal_error(str(e))