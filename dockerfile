FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./

COPY tsconfig.json tsconfig.build.json README.md values.tpl.yaml nest-cli.json ./

RUN npm install

COPY ./src  ./src

RUN npm run build


FROM node:22-alpine

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY --from=build /app/package.json ./package.json
COPY --from=build /app/package-lock.json ./package-lock.json

RUN npm ci --omit=dev
RUN apk add --no-cache curl


EXPOSE 3000


CMD [ "npm", "run", "start:prod"]