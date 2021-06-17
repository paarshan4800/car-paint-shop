# Car Paint Shop API

---

- Shop has four painting areas (red, blue, yellow, green).
- The whole shop has only a queue. Only a car in the front can get into the painting area.
- It takes 20 seconds to paint a car. If a car is in a painting area, and the next car requested the same color and all
  the cars should wait.
- Admin can set the queue length, and close any painting area if that specific color paint is over or out of stock. (
  Cars that got into the queue can get painted, only new cars requesting that color can’t get in).
- A set of admin routes for setting the queue length, closing and opening painting areas.
- A set of user routes to request painting jobs and see available jobs.
- Authentication features like login, register, forgot and reset password with Two-Factor authentication, Google Login,
  Email verification and route protection are implemented.

## API Docs

- [Postman Documentation](https://car-paint-shop.herokuapp.com/api-docs)

## Hosted URL

- [Car Paint Shop API](https://car-paint-shop.herokuapp.com)

## Admin Login Credentials

Email | Password
------------ | -------------
admin1@gmail.com | admin1@password
admin2@gmail.com | admin2@password
admin3@gmail.com | admin3@password

