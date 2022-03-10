import axios from 'axios';

const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0NjkwNjIxNiwianRpIjoiODQxNDkxM2EtY2FkNy00MjcyLWE1NjItYTg0YzAwZjg1MDU2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImNvbnJhZCIsIm5iZiI6MTY0NjkwNjIxNiwiZXhwIjoxNjQ2OTkyNjE2fQ.KL79ol1acXoJmLHhKVb49ZBSeRoIwYwtj6oE_b4kaug"
export default axios.create({
	baseURL: `http://127.0.0.1:8899/`,
	headers: {
		Authorization: `Bearer `+token
	}
});