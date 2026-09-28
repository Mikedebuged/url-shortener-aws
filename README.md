# url-shortener-aws
# URL Shortener on AWS

A URL shortener API built with Python and FastAPI, which I'm taking from local code to an automated AWS deployment.

## Status

- [x] API with health check, shorten, and redirect endpoints
- [x] Automated tests with pytest
- [ ] Containerized with Docker
- [ ] CI pipeline with GitHub Actions
- [ ] AWS infrastructure defined in Terraform
- [ ] Automatic deployment and CloudWatch monitoring

## Run it locally

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pytest
    uvicorn app.main:app --reload

Then open http://localhost:8000/docs
