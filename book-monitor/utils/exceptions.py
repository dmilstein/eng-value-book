"""Custom exceptions for the book monitor application."""


class BookMonitorException(Exception):
    """Base exception class for all book monitor errors."""
    
    def __init__(self, message: str, details: str = None):
        """Initialize exception with message and optional details.
        
        Args:
            message: Human-readable error message
            details: Optional additional details about the error
        """
        super().__init__(message)
        self.message = message
        self.details = details
    
    def __str__(self):
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class FileNotFoundError(BookMonitorException):
    """Exception raised when a required file is not found."""
    
    def __init__(self, file_path: str, details: str = None):
        """Initialize with file path and optional details.
        
        Args:
            file_path: Path to the missing file
            details: Optional additional details
        """
        message = f"File not found: {file_path}"
        super().__init__(message, details)
        self.file_path = file_path


class ParseError(BookMonitorException):
    """Exception raised when parsing fails."""
    
    def __init__(self, file_path: str, line_number: int = None, details: str = None):
        """Initialize with file path, optional line number and details.
        
        Args:
            file_path: Path to the file that failed to parse
            line_number: Optional line number where parsing failed
            details: Optional additional details about the parse error
        """
        if line_number:
            message = f"Parse error in {file_path} at line {line_number}"
        else:
            message = f"Parse error in {file_path}"
        super().__init__(message, details)
        self.file_path = file_path
        self.line_number = line_number


class ConfigError(BookMonitorException):
    """Exception raised when configuration is invalid."""
    
    def __init__(self, config_key: str = None, details: str = None):
        """Initialize with optional config key and details.
        
        Args:
            config_key: Optional configuration key that is invalid
            details: Optional additional details about the config error
        """
        if config_key:
            message = f"Configuration error for key '{config_key}'"
        else:
            message = "Configuration error"
        super().__init__(message, details)
        self.config_key = config_key
