# Chicken Rice

We'll call it this until we finally figure out what to call the project. Bryan came up with the name, so kill him not me

# Contributing

Please create a folder per project. Then work on your own folders. Use branches. Thanks.

# Current Problems

Backend contacts ML in a straightforward fashion. If ML takes time to process events, so will the Lambda function. A viable method to solve this may be via a queue, or some other methods. Also, since each image from the devices are unique despite containing the same event ID, duplicates of the same event ID might get processed by the backend. Using a managed queue like AWS SQS can unnecessary duplicate processing.
