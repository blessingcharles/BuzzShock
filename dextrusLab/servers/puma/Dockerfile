FROM ruby:3.1.2
WORKDIR /app
COPY Gemfile Gemfile.lock ./
RUN bundle install
COPY . .
CMD ["bundle", "exec", "puma", "-b", "tcp://0.0.0.0:80"]
