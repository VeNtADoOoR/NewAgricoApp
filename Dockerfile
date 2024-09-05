# Use an official PHP runtime as a parent image
FROM php:8.3-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gdal-bin \
    git \
    unzip \
    zip \
    && docker-php-ext-install pdo pdo_mysql

# Install GDAL PHP bindings (optional, depending on use)
#RUN pecl install gdal \
#    && docker-php-ext-enable gdal

# Set the working directory inside the container
WORKDIR /var/www/html

# Copy existing application directory contents
COPY . /var/www/html

# Install Composer and Laravel dependencies
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN composer install

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]