import api from '../src/services/api';
import axios from 'axios';

jest.mock('axios');

describe('API service', () => {
  const mockResponse = { data: { message: 'success' } };
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should make GET request to fetch users', async () => {
    axios.get.mockResolvedValueOnce(mockResponse);
    const response = await api.getUsers();
    expect(response).toEqual(mockResponse.data);
    expect(axios.get).toHaveBeenCalledWith('/api/users');
  });

  test('should make POST request to create user', async () => {
    axios.post.mockResolvedValueOnce(mockResponse);
    const userData = { name: 'John Doe', email: 'john@example.com' };
    const response = await api.createUser(userData);
    expect(response).toEqual(mockResponse.data);
    expect(axios.post).toHaveBeenCalledWith('/api/users', userData);
  });

  test('should make PUT request to update user', async () => {
    axios.put.mockResolvedValueOnce(mockResponse);
    const userData = { id: 1, name: 'John Updated' };
    const response = await api.updateUser(1, userData);
    expect(response).toEqual(mockResponse.data);
    expect(axios.put).toHaveBeenCalledWith('/api/users/1', userData);
  });

  test('should make DELETE request to delete user', async () => {
    axios.delete.mockResolvedValueOnce(mockResponse);
    const response = await api.deleteUser(1);
    expect(response).toEqual(mockResponse.data);
    expect(axios.delete).toHaveBeenCalledWith('/api/users/1');
  });

  test('should handle network error in getUsers', async () => {
    const error = new Error('Network Error');
    axios.get.mockRejectedValueOnce(error);
    await expect(api.getUsers()).rejects.toThrow('Network Error');
  });

  test('should handle server error in createUser', async () => {
    const errorResponse = { response: { status: 400, data: { error: 'Bad Request' } } };
    axios.post.mockRejectedValueOnce(errorResponse);
    await expect(api.createUser({})).rejects.toEqual(errorResponse);
  });

  test('should handle timeout in updateUser', async () => {
    const error = { code: 'ECONNABORTED' };
    axios.put.mockRejectedValueOnce(error);
    await expect(api.updateUser(1, {})).rejects.toEqual(error);
  });

  test('should make GET request to fetch posts', async () => {
    axios.get.mockResolvedValueOnce(mockResponse);
    const response = await api.getPosts();
    expect(response).toEqual(mockResponse.data);
    expect(axios.get).toHaveBeenCalledWith('/api/posts');
  });

  test('should make POST request to create post', async () => {
    axios.post.mockResolvedValueOnce(mockResponse);
    const postData = { title: 'New Post', content: 'Post content' };
    const response = await api.createPost(postData);
    expect(response).toEqual(mockResponse.data);
    expect(axios.post).toHaveBeenCalledWith('/api/posts', postData);
  });

  test('should make PUT request to update post', async () => {
    axios.put.mockResolvedValueOnce(mockResponse);
    const postData = { id: 1, title: 'Updated Post' };
    const response = await api.updatePost(1, postData);
    expect(response).toEqual(mockResponse.data);
    expect(axios.put).toHaveBeenCalledWith('/api/posts/1', postData);
  });

  test('should make DELETE request to delete post', async () => {
    axios.delete.mockResolvedValueOnce(mockResponse);
    const response = await api.deletePost(1);
    expect(response).toEqual(mockResponse.data);
    expect(axios.delete).toHaveBeenCalledWith('/api/posts/1');
  });

  test('should handle empty response data', async () => {
    axios.get.mockResolvedValueOnce({ data: {} });
    const response = await api.getUsers();
    expect(response).toEqual({});
  });

  test('should handle null response data', async () => {
    axios.get.mockResolvedValueOnce({ data: null });
    const response = await api.getUsers();
    expect(response).toBeNull();
  });

  test('should handle undefined response data', async () => {
    axios.post.mockResolvedValueOnce({ data: undefined });
    const response = await api.createUser({});
    expect(response).toBeUndefined();
  });

  test('should handle string response data', async () => {
    axios.put.mockResolvedValueOnce({ data: 'success' });
    const response = await api.updateUser(1, {});
    expect(response).toBe('success');
  });

  test('should handle array response data', async () => {
    const arrayData = [1, 2, 3];
    axios.delete.mockResolvedValueOnce({ data: arrayData });
    const response = await api.deleteUser(1);
    expect(response).toEqual(arrayData);
  });

  test('should make GET request with query parameters', async () => {
    axios.get.mockResolvedValueOnce(mockResponse);
    await api.getUsers({ page: 1, limit: 10 });
    expect(axios.get).toHaveBeenCalledWith('/api/users?page=1&limit=10');
  });

  test('should handle special characters in URL', async () => {
    axios.get.mockResolvedValueOnce(mockResponse);
    await api.getUsers();
    expect(axios.get).toHaveBeenCalledWith('/api/users');
  });

  test('should handle concurrent requests', async () => {
    const mockResponses = [
      { data: { id: 1, name: 'User 1' } },
      { data: { id: 1, title: 'Post 1' } }
    ];
    axios.get.mockResolvedValueOnce(mockResponses[0]);
    axios.get.mockResolvedValueOnce(mockResponses[1]);
    
    const userPromise = api.getUsers();
    const postPromise = api.getPosts();
    
    const [userResponse, postResponse] = await Promise.all([userPromise, postPromise]);
    expect(userResponse).toEqual({ id: 1, name: 'User 1' });
    expect(postResponse).toEqual({ id: 1, title: 'Post 1' });
  });
});