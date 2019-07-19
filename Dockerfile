FROM golang:1.12-alpine3.10 as builder

WORKDIR /go/src/vsphere-influxdb-go
COPY . .
RUN apk --update add --virtual build-deps git 
RUN go get -d -v ./...
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo

FROM alpine:3.10
RUN apk update \
 && apk upgrade \
 && apk add ca-certificates \
 && addgroup -S spock && adduser -S spock -G spock
COPY --from=0 /go/src/vsphere-influxdb-go/vsphere-influxdb-go /vsphere-influxdb-go

USER spock

CMD ["/vsphere-influxdb-go"]
