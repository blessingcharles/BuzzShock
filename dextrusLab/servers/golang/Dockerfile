FROM golang
USER root
WORKDIR /go/src/app
COPY server.go /go/src/app/server.go
RUN go mod init
RUN go build .
CMD ["./app"]
