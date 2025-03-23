# Sparse Optical Flow

# Implementing the Pyramidal Approach

---

<p align="center">
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/DrawNote_rough_2503061648216.jpg" width="500px"/>
</p>

Here let’s suppose that we have a matrix of 9 cross 9 and each box corresponds to an array which contains three things - Ix, Iy and It. When the “go_to_upper_level” is used then the set of each 3 cross 3 matrix inside this 9 cross 9 matrix (i.e. a total of 9 sets) are averaged. That means that each element of the yellow colored 3 cross 3 matrix is averaged to find a single value which is then placed in the yellow colored box of the above matrix. This is how a matrix of the size of n cross n is converted to  **√n cross √n size. However in case of “go_to_lower_level”, I have not used any concept of average. Instead I have used the actual values of Ix, Iy and Iz (which can be calculated by the previous and next frame).** 

## Need of going up/down levels

---

The need of going from lower to upper level is the concept of pyramidal approach as was mentioned in the Lucas-Kanade algorithm doc.

The need of going a level down was that in many cases the determinant of the matrix M came out to be zero. In such cases, the code goes down a few levels until either the determinant of M becomes non-zero or the “current_count” (which is the number of levels the code has gone down) reaches the “max_count” (which is the limit of going down, defined in the LK_params) is reached. In case the max_count limit is reached and still the determinant of M is zero, then the code returns the original point as the final point. This causes a single point on the screen instead of lines and this causes discontinuity.

<p align="center">
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/DrawNote_rough_2503061706093.jpg" width="600px"/>
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/image.png" width=600px/>
</p>

## Eigenvalue Conditions

A few conditions related to the eigenvalues of the Matrix M are important so that the algorithm works good. The conditions are : 

<p align="center">
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/image%201.png" width=400px/>
</p>
Here the matrix A * A transpose is actually M only and thus the eigenvalues of M are lambda1 and lambda2

<p align="center">
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/64eee7ac-8302-415d-a083-5694733f7b1b.png" width=300px/>
</p>
These two parameters epsilon_lower and epsilon_higher are passed in the lk_params

## What points are joined to form a line?

The actual algorithm is that the function “LK” takes 4 parameters - previous frame, next frame, red points (corner points) of the previous frame and the lk_params (which is a set of parameters for the things mentioned above). Now the code finds the values of Ix, Iy and It for all the points in the defined neighborhood of the red points (The neighborhood is defined by the parameter window size). Now, depending upon the value of the maxLevel, it goes up a few levels to saturate the image and the values of Ix, Iy and It by using the average method as mentioned above. Now, it finds the value of v_x and v_y and then return the new_point as :

<p align="center">
  <img src="https://raw.githubusercontent.com/saxenatanishq/Sparse-Optical-Flow/refs/heads/main/Photos%20and%20Videos/DrawNote_rough_2503061727323.jpg" width=400px/>
</p>
The line is then drawn between the points (x, y) and (new x, new y). This is also a reason of discontinuity (because instead of joining the previous point to the new location of the point, I am joining the previous point to the expected position of the previous point)
