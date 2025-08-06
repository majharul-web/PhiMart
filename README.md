# PhiMart - An E-Commerce DRF Application

PhiMart is a comprehensive e-commerce application built using Django Rest Framework (DRF). It provides a robust backend for managing products, orders, and user accounts, making it suitable for building online shopping platforms.

## Features

- **User** authentication and registration
- **Product** management (CRUD operations)
- **Order** management (create, view, and manage orders)
- **Cart** management
- **Search** functionality for products
- **Pagination** for product listings
- **Admin** interface for managing products and orders

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/majharul-web/PhiMart.git
   ```
   Navigate to the project directory:
   ```bash
   cd PhiMart
   ```
2. Create a virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the application at `http://localhost:8000/`

## API Documentation

API documentation is available at `http://localhost:8000/api/swagger/` when the server is running. It provides detailed information about the available endpoints, request parameters, and response formats.

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature or fix description"
   ```
4. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the project
maintainer at [majharul.dev.alt@gmail.com](mailto:majharul.dev.alt@gmail.com)

## Acknowledgements

- Thanks to the Django and Django Rest Framework communities for their excellent documentation and support.
- Inspired by various e-commerce platforms and best practices in web development.
