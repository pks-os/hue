
FROM ubuntu:18.04 as build
LABEL description="gethue.com website"

RUN apt-get update -y && apt-get install -y \
  wget \
  python-pip

RUN wget https://github.com/gohugoio/hugo/releases/download/v0.62.0/hugo_0.62.0_Linux-64bit.deb \
  && dpkg -i hugo*.deb \
  && rm hugo*.deb \
  && pip install Pygments

ADD gethue /gethue
WORKDIR /gethue

RUN hugo --baseURL ""



FROM nginx:1.17-alpine
COPY --from=build /gethue/public /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
