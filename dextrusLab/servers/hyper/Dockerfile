FROM rust
WORKDIR /app
COPY src /app/src
COPY Cargo.toml .
RUN cargo build --release
CMD ["/app/target/release/hyper"]
