"""Error handling utilities for Flask application."""

import logging
from flask import render_template, jsonify, request
from utils.exceptions import BookMonitorException, FileNotFoundError, ParseError, ConfigError


def setup_error_handlers(app):
    """Set up error handlers for the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(404)
    def handle_404(error):
        """Handle 404 Not Found errors."""
        app.logger.warning(f"404 error: {request.url}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Not Found',
                'message': 'The requested resource was not found.',
                'status_code': 404
            }), 404
        
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f"500 error: {str(error)}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Internal Server Error',
                'message': 'An internal server error occurred.',
                'status_code': 500
            }), 500
        
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(BookMonitorException)
    def handle_book_monitor_exception(error):
        """Handle custom BookMonitorException errors."""
        app.logger.error(f"BookMonitor error: {str(error)}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Book Monitor Error',
                'message': error.message,
                'details': error.details,
                'status_code': 400
            }), 400
        
        return render_template('error.html', 
                             error_message=str(error)), 400
    
    @app.errorhandler(FileNotFoundError)
    def handle_file_not_found(error):
        """Handle FileNotFoundError exceptions."""
        app.logger.warning(f"File not found: {error.file_path}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'File Not Found',
                'message': error.message,
                'file_path': error.file_path,
                'status_code': 404
            }), 404
        
        return render_template('error.html', 
                             error_message=f"Required file not found: {error.file_path}"), 404
    
    @app.errorhandler(ParseError)
    def handle_parse_error(error):
        """Handle ParseError exceptions."""
        app.logger.error(f"Parse error: {str(error)}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Parse Error',
                'message': error.message,
                'file_path': error.file_path,
                'line_number': error.line_number,
                'status_code': 400
            }), 400
        
        return render_template('error.html', 
                             error_message=f"Failed to parse file: {error.file_path}"), 400
    
    @app.errorhandler(ConfigError)
    def handle_config_error(error):
        """Handle ConfigError exceptions."""
        app.logger.error(f"Configuration error: {str(error)}")
        
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Configuration Error',
                'message': error.message,
                'config_key': error.config_key,
                'status_code': 500
            }), 500
        
        return render_template('error.html', 
                             error_message=f"Configuration error: {error.message}"), 500


def configure_logging(app):
    """Configure logging for the application.
    
    Args:
        app: Flask application instance
    """
    if not app.debug:
        # Production logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('book_monitor.log')
            ]
        )
    else:
        # Development logging configuration
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(funcName)s:%(lineno)d]'
        )
    
    # Set specific log levels for different modules
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
