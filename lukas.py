import cv2 as cv
import numpy as np
import math

def LK(prev_frame, new_frame, prev_green,**lk_params):
    winsize = lk_params['winsize']
    maxlevel = lk_params['maxLevel']
    epsilon_lower = lk_params['epsilon_lower']
    epsilon_higher = lk_params['epsilon_higher']
    max_count = lk_params['max_count']
    fps = lk_params['fps']
    t = 1/fps

    def find_I(new_frame, prev_frame, point):
        x,y = int(point[0]), int(point[1])
        if x + 1 >= prev_frame.shape[0] or y + 1 >= prev_frame.shape[1]: # In case the green point is the edge of the screen
            return 0, 0, 0
        Ix = prev_frame[x + 1, y] - prev_frame[x, y]
        Iy = prev_frame[x, y + 1] - prev_frame[x, y]
        It = new_frame[x, y] - prev_frame[x, y]
        return Ix, Iy, It
    
    def inverse(matrix):
        try:
            matrix = np.array(matrix, dtype=float)
            return np.linalg.inv(matrix)
        except np.linalg.LinAlgError:
            raise ValueError("Matrix is singular and cannot be inverted.")
    
    def go_to_upper_level(neighbour_array):
        prev_size = neighbour_array.shape[0]
        new_size = int(math.sqrt(prev_size))
        new_neighbour_array = np.zeros((new_size, new_size, 3))
        for i in range(0,prev_size,new_size):
            for j in range(0,prev_size,new_size):
                average_Ix = np.sum(neighbour_array[i:i+new_size, j:j+new_size, 0])/new_size
                average_Iy = np.sum(neighbour_array[i:i+new_size, j:j+new_size, 1])/new_size
                average_It = np.sum(neighbour_array[i:i+new_size, j:j+new_size, 2])/new_size
                new_neighbour_array[i//new_size, j//new_size] = (average_Ix, average_Iy, average_It)
        
        return new_neighbour_array
    
    def go_to_lower_level(neighbour_array, point):
        prev_size = neighbour_array.shape[0]
        new_size = prev_size**2
        new_neighbour_array = np.zeros((new_size, new_size, 3))
        for i in range(new_size):
            for j in range(new_size):
                x = point[0] - new_size // 2 + i
                y = point[1] - new_size // 2 + j
                if x < 0 or y < 0 or x >= prev_frame.shape[0] or y >= prev_frame.shape[1]:
                    new_neighbour_array[i, j] = (0, 0, 0)
                else:
                    Ix, Iy, It = find_I(new_frame, prev_frame, (x, y))
                    new_neighbour_array[i, j] = (Ix, Iy, It)
        return new_neighbour_array

    def check_epsilon_conditions(M):
        eigenvalues, matrix = np.linalg.eig(M)
        lambda1, lambda2 = eigenvalues
        if np.minimum(lambda1, lambda2) < epsilon_lower:
            return False
        if np.maximum(lambda1, lambda2)/np.minimum(lambda1, lambda2) > epsilon_higher:
            return False
        return True

    next_points = []
    mod_count = 0
    epsilon_count = 0

    for point in prev_green:
        neighbour_array = np.zeros((winsize, winsize, 3))
        point = point.ravel()
        
        for i in range(winsize):
            for j in range(winsize):
                Ix, Iy, It = find_I(new_frame, prev_frame, (point[0] - winsize//2 + i, point[1] - winsize//2 + j))
                neighbour_array[i][j] = (Ix, Iy, It)
        
        for j in range(maxlevel-1):
            neighbour_array = go_to_upper_level(neighbour_array)

        current_count = 0
        while(current_count != max_count):
            M = np.zeros((2, 2))
            N = np.zeros((2, 1))
            for i in range(len(neighbour_array)):
                for j in range(len(neighbour_array)):
                    M[0, 0] += neighbour_array[i, j, 0]**2
                    M[0, 1] += neighbour_array[i, j, 0]*neighbour_array[i, j, 1]
                    M[1, 0] =  M[0, 1]
                    M[1, 1] += neighbour_array[i, j, 1]**2
                    N[0, 0] -= neighbour_array[i, j, 0] * neighbour_array[i, j, 2]
                    N[1, 0] -= neighbour_array[i, j, 1] * neighbour_array[i, j, 2]
            
            if np.linalg.det(M) != 0 and check_epsilon_conditions(M):
                M_inverse = inverse(M)
                V = np.matmul(M_inverse,N)
                v_x = V[0].item()
                v_y = V[1].item()
                expected_point = [point[0]+v_x*t, point[1]+v_y*t]
                break
            elif np.linalg.det(M) == 0:
                mod_count+=1
            else:
                epsilon_count += 1
        
            neighbour_array = go_to_lower_level(neighbour_array, point)    
            current_count += 1
        
        if current_count == max_count:
            expected_point = point
        
        next_points.append(expected_point)
    
    print(f"mod = {mod_count} and condition = {epsilon_count}")
    next_points = np.array(next_points)
    return next_points