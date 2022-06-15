#FROM node:16.14.2
#
#WORKDIR /app
#
##ENV PATH /app/node_modules/.bin:$PATH
#
#COPY package.json /app/package.json
#RUN npm install --legacy-peer-deps
#
#COPY . /app
#
#CMD npm start

FROM node:16.14.2
# WORKDIR /app
WORKDIR /react
COPY package.json ./
COPY package-lock.json ./
COPY ./ ./
# RUN npm install --legacy-peer-deps
# CMD npm start
RUN rm -rf node_modules
RUN npm install --legacy-peer-deps
RUN npm run build


# CMD ["npm", "run", "build"]