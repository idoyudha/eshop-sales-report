# Sales Report Service
Part of [eshop](https://github.com/idoyudha/eshop) Microservices Architecture.

## Overview
This service focusing handle sales report, which created after order is successfull paid by customer and accepted by the admin. Only admin role can access this service. Currently, admin can view all the sales and download the report in excel format (xlsx).

### Architecture
```
eshop-auth
├── .github/
│   └── workflows/      # github workflows to automatically test, build, and push
└── app/   
    ├── api/            
    │   └── routes/     # http endpoint routes
    ├── constants/      # constant that can be reuse
    ├── core/           # general config like env and database initialization
    ├── event/          # event subscriber
    ├── migration/      # sql migration
    ├── models/         # entities of business logic (models) can be used in any layer
    ├── repository/     # abstract storage (database) that business logic works with
    ├── service/        # business logic
    └── utils/          # helpers function
```

### Tech Stack
- Programming Language: Python
- Framework: FastAPI
- Database: PostgreSQL
- Authentication: AWS Cognito
- Message Broker: Apache Kafka
- Container: Docker