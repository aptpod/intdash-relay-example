FROM alpine:3.22

RUN apk add --no-cache ca-certificates tzdata

COPY relayd /relayd

RUN chmod +x /relayd

RUN addgroup -g 1000 relayd && \
    adduser -D -s /bin/sh -u 1000 -G relayd relayd

RUN mkdir -p /etc/relayd && \
    chown relayd:relayd /etc/relayd

USER relayd

EXPOSE 8080

ENTRYPOINT ["/relayd", "serve", "-c", "/etc/relayd/relayd.conf"]
