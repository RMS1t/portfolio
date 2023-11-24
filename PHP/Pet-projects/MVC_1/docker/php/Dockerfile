FROM php:8.1-fpm-alpine

WORKDIR /pop-it-mvc


RUN apk update && apk add \
    vim \
    bash \
    curl


RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

RUN curl -sSLf \
            -o /usr/local/bin/install-php-extensions \
            https://github.com/mlocati/docker-php-extension-installer/releases/latest/download/install-php-extensions
RUN chmod +x /usr/local/bin/install-php-extensions
RUN install-php-extensions \
            pdo \
            pdo_pgsql

RUN apk add --no-cache linux-headers  \
    && apk add --update --no-cache --virtual .build-dependencies $PHPIZE_DEPS \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug \
    && pecl clear-cache \
    && apk del .build-dependencies

ADD ./php.ini /usr/local/etc/php/conf.d/40-custom.ini

COPY . .



EXPOSE 9000


CMD ["php-fpm"]


