import pytest
import logging
import time
from api_clients.multimodal_models import MultimodalModelsAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_gemini_2_5_pro_200_requests(login_as_user):
    """Test sending 200 consecutive requests to Gemini 2.5 Pro model."""
    user_config = login_as_user("Member4")  # eng tier3
    
    multimodal_api = MultimodalModelsAPI(user_config)
    
    # Test parameters
    total_requests = 200
    prompt = """Hi I need help with a complex software development project. I'm working on a large-scale web application using React, Node.js, and PostgreSQL. The application needs to handle user authentication, real-time data synchronization, payment processing, and advanced analytics. 

I'm facing several challenges:
1. Performance optimization for handling millions of database queries
2. Implementing secure authentication with JWT tokens and OAuth2
3. Building a scalable microservices architecture
4. Integrating third-party APIs for payment processing
5. Implementing real-time notifications using WebSockets
6. Creating comprehensive unit and integration tests
7. Setting up CI/CD pipelines with Docker and Kubernetes
8. Implementing caching strategies with Redis
9. Building responsive UI components with accessibility features
10. Managing state with Redux and handling complex data flows

Could you please provide detailed guidance on best practices, code examples, architectural patterns, and step-by-step implementation strategies for each of these areas? I need comprehensive explanations with practical examples that I can implement in my project."""
    system_message = """You are an expert software architect and senior full-stack developer with 15+ years of experience in building enterprise-grade applications. You specialize in React, Node.js, PostgreSQL, microservices architecture, cloud deployment, and DevOps practices. 

Please provide detailed, practical, and actionable advice with code examples, architectural diagrams, and implementation strategies. Focus on scalability, security, performance, and maintainability. Include specific libraries, tools, and frameworks you recommend, along with their pros and cons."""
    model_name = "gemini-2.5-pro"
    
    logger.info(f"🚀 Starting {total_requests} consecutive requests to {model_name}")
    logger.info(f"User: Member4 (eng tier3)")
    logger.info(f"Prompt length: {len(prompt)} characters")
    
    # Track results
    successful_requests = 0
    failed_requests = 0
    total_response_time = 0
    errors = []
    
    start_time = time.time()
    
    for i in range(total_requests):
        try:
            request_start = time.time()
            
            response = multimodal_api.call_model(
                model_name=model_name,
                prompt=prompt,
                system_message=system_message
            )
            
            request_end = time.time()
            request_duration = request_end - request_start
            total_response_time += request_duration
            
            # Validate response
            assert response is not None, f"Request {i+1}: Response should not be None"
            assert "choices" in response, f"Request {i+1}: Response should contain 'choices' field. Got: {response}"
            assert len(response["choices"]) > 0, f"Request {i+1}: Response should have at least one choice"
            
            content = response["choices"][0]["message"]["content"]
            assert len(content) > 0, f"Request {i+1}: Response content should not be empty"
            assert isinstance(content, str), f"Request {i+1}: Response content should be a string"
            
            successful_requests += 1
            
            # Log progress every 40 requests
            if (i + 1) % 40 == 0:
                logger.info(f"✅ Completed {i+1}/{total_requests} requests (Success: {successful_requests}, Failed: {failed_requests})")
            
        except Exception as e:
            failed_requests += 1
            error_msg = f"Request {i+1}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"❌ {error_msg}")
            
            # Stop if too many failures
            if failed_requests > 10:
                logger.error(f"🛑 Too many failures ({failed_requests}), stopping test")
                break
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Calculate statistics
    success_rate = (successful_requests / total_requests) * 100
    avg_response_time = total_response_time / successful_requests if successful_requests > 0 else 0
    requests_per_second = total_requests / total_duration if total_duration > 0 else 0
    
    # Log final results
    logger.info(f"📊 Test Results:")
    logger.info(f"   Total Requests: {total_requests}")
    logger.info(f"   Successful: {successful_requests}")
    logger.info(f"   Failed: {failed_requests}")
    logger.info(f"   Success Rate: {success_rate:.2f}%")
    logger.info(f"   Total Duration: {total_duration:.2f} seconds")
    logger.info(f"   Average Response Time: {avg_response_time:.2f} seconds")
    logger.info(f"   Requests Per Second: {requests_per_second:.2f}")
    
    # Assertions
    assert successful_requests >= 180, f"Expected at least 180 successful requests, got {successful_requests}"
    assert success_rate >= 90.0, f"Expected success rate >= 90%, got {success_rate:.2f}%"
    assert failed_requests <= 20, f"Expected <= 20 failed requests, got {failed_requests}"
    
    # Log first few errors if any
    if errors:
        logger.info(f"🔍 First 5 errors:")
        for error in errors[:5]:
            logger.info(f"   {error}")
    
    logger.info(f"✅ Test completed successfully!")

def test_gemini_2_5_pro_200_requests_with_delay(login_as_user):
    """Test sending 200 requests to Gemini 2.5 Pro with 0.1s delay between requests."""
    user_config = login_as_user("Member4")  # eng tier3
    
    multimodal_api = MultimodalModelsAPI(user_config)
    
    # Test parameters
    total_requests = 200
    delay_seconds = 0.1
    prompt = """Hi I need help with a complex software development project. I'm working on a large-scale web application using React, Node.js, and PostgreSQL. The application needs to handle user authentication, real-time data synchronization, payment processing, and advanced analytics. 

I'm facing several challenges:
1. Performance optimization for handling millions of database queries
2. Implementing secure authentication with JWT tokens and OAuth2
3. Building a scalable microservices architecture
4. Integrating third-party APIs for payment processing
5. Implementing real-time notifications using WebSockets
6. Creating comprehensive unit and integration tests
7. Setting up CI/CD pipelines with Docker and Kubernetes
8. Implementing caching strategies with Redis
9. Building responsive UI components with accessibility features
10. Managing state with Redux and handling complex data flows

Could you please provide detailed guidance on best practices, code examples, architectural patterns, and step-by-step implementation strategies for each of these areas? I need comprehensive explanations with practical examples that I can implement in my project."""
    system_message = """You are an expert software architect and senior full-stack developer with 15+ years of experience in building enterprise-grade applications. You specialize in React, Node.js, PostgreSQL, microservices architecture, cloud deployment, and DevOps practices. 

Please provide detailed, practical, and actionable advice with code examples, architectural diagrams, and implementation strategies. Focus on scalability, security, performance, and maintainability. Include specific libraries, tools, and frameworks you recommend, along with their pros and cons."""
    model_name = "gemini-2.5-pro"
    
    logger.info(f"🚀 Starting {total_requests} requests to {model_name} with {delay_seconds}s delay")
    logger.info(f"User: Member4 (eng tier3)")
    logger.info(f"Prompt length: {len(prompt)} characters")
    
    # Track results
    successful_requests = 0
    failed_requests = 0
    total_response_time = 0
    errors = []
    
    start_time = time.time()
    
    for i in range(total_requests):
        try:
            request_start = time.time()
            
            response = multimodal_api.call_model(
                model_name=model_name,
                prompt=prompt,
                system_message=system_message
            )
            
            request_end = time.time()
            request_duration = request_end - request_start
            total_response_time += request_duration
            
            # Validate response
            assert response is not None, f"Request {i+1}: Response should not be None"
            assert "choices" in response, f"Request {i+1}: Response should contain 'choices' field. Got: {response}"
            assert len(response["choices"]) > 0, f"Request {i+1}: Response should have at least one choice"
            
            content = response["choices"][0]["message"]["content"]
            assert len(content) > 0, f"Request {i+1}: Response content should not be empty"
            assert isinstance(content, str), f"Request {i+1}: Response content should be a string"
            
            successful_requests += 1
            
            # Log progress every 40 requests
            if (i + 1) % 40 == 0:
                logger.info(f"✅ Completed {i+1}/{total_requests} requests (Success: {successful_requests}, Failed: {failed_requests})")
            
        except Exception as e:
            failed_requests += 1
            error_msg = f"Request {i+1}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"❌ {error_msg}")
            
            # Stop if too many failures
            if failed_requests > 10:
                logger.error(f"🛑 Too many failures ({failed_requests}), stopping test")
                break
        
        # Add delay between requests
        if i < total_requests - 1:  # Don't delay after last request
            time.sleep(delay_seconds)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Calculate statistics
    success_rate = (successful_requests / total_requests) * 100
    avg_response_time = total_response_time / successful_requests if successful_requests > 0 else 0
    requests_per_second = total_requests / total_duration if total_duration > 0 else 0
    
    # Log final results
    logger.info(f"📊 Test Results (with {delay_seconds}s delay):")
    logger.info(f"   Total Requests: {total_requests}")
    logger.info(f"   Successful: {successful_requests}")
    logger.info(f"   Failed: {failed_requests}")
    logger.info(f"   Success Rate: {success_rate:.2f}%")
    logger.info(f"   Total Duration: {total_duration:.2f} seconds")
    logger.info(f"   Average Response Time: {avg_response_time:.2f} seconds")
    logger.info(f"   Requests Per Second: {requests_per_second:.2f}")
    
    # Assertions
    assert successful_requests >= 190, f"Expected at least 190 successful requests, got {successful_requests}"
    assert success_rate >= 95.0, f"Expected success rate >= 95%, got {success_rate:.2f}%"
    assert failed_requests <= 10, f"Expected <= 10 failed requests, got {failed_requests}"
    
    # Log first few errors if any
    if errors:
        logger.info(f"🔍 First 5 errors:")
        for error in errors[:5]:
            logger.info(f"   {error}")
    
    logger.info(f"✅ Test completed successfully!")
