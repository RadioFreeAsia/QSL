FROM node:16-slim as base
FROM base as builder

RUN apt-get update \
    && buildDeps="python3 build-essential" \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=node . /build/
RUN corepack enable

USER node
WORKDIR /build
RUN yarn install --network-timeout 1000000 \
    && yarn build

FROM base

LABEL maintainer="Michael McFadden <mcfaddenm@rfa.org>" \
      org.label-schema.name="rfaqsl-frontend" \
      org.label-schema.description="RFA QSL frontend image." \
      org.label-schema.vendor="Michael McFadden"

RUN apt-get update \
    && buildDeps="busybox" \
    && apt-get install -y --no-install-recommends $buildDeps \
    && busybox --install -s \
    && rm -rf /var/lib/apt/lists/*

USER node
COPY --from=builder /build/ /app/

WORKDIR /app
EXPOSE 3000
CMD ["yarn", "start:prod"]
