import numpy as np
import matplotlib.pyplot as plt

class VMMGenerator():
    '''
    Object for modeling motion - based on section 5.3 of the Probabilistic Robotics text
    '''
    #TODO: test model with higher dimension motion, currently only [x, y, theta] and [v, w] motion is supported 


    def __init__(self, alpha):
        '''contructor to set alpha motion uncertainties'''
        self._a_1, self._a_2, self._a_3, self._a_4, self._a_5, self._a_6 = alpha
        pass

    def motion_model_velocity(self, pose, command, pose_prime, d_time):
        '''
        This method has not been tested
        pose - [x, y, theta] describing the objects position and orientation
        command - [v, w] describing the input command in terms of linear and rotational velocity
        pose_prime - [x, y, theta] describing the expected position and orientation after applying the command

        returns the probability of object taking the pose_prime position
        '''

        _x, _y, _theta = pose    
        _x_p, _y_p, _theta_p = pose_prime
        _v, _w = command

        #standardize the         
        if _theta_p > np.pi:
            _theta_p -= np.pi*2
        elif _theta_p < -np.pi:
            _theta_p += np.pi*2
        
        mu = 0.5 * ( (_x - _x_p) * np.cos(_theta) + (_y - _y_p) * np.sin(_theta) ) / ( (_y - _y_p) * np.cos(_theta) - (_x - _x_p) * np.sin(_theta) )
        
        if np.isinf(mu):
            mu = - np.abs(_x - _x_p)
        if np.isneginf(mu):
            mu = np.abs(_x - _x_p)
        
        x_star = (_x + _x_p) / 2 + mu * (_y - _y_p)
        y_star = (_y + _y_p) / 2 + mu * (_x_p - _x)
        r_star = np.sqrt((_x - x_star)**2 + (_y - y_star)**2)

        d_theta = np.arctan2(_y_p - y_star, _x_p - x_star) - np.arctan2(_y - y_star, _x - x_star)
        
        if d_theta < -np.pi/2 :
            d_theta += 2*np.pi

        v_hat = d_theta / d_time * r_star
        w_hat = d_theta / d_time
        gamma_hat = (_theta_p - _theta) / d_time - w_hat

        v_prob = self.prob_normal_distribution(_v - v_hat, self._a_1 * np.abs(_v) + self._a_2 * np.abs(_w))
        w_prob = self.prob_normal_distribution(_w - w_hat, self._a_3 * np.abs(_v) + self._a_4 * np.abs(_w))
        gamma_prob = self.prob_normal_distribution(gamma_hat, self._a_5 * np.abs(_v) + self._a_6 * np.abs(_w))
        
        return v_prob * w_prob * gamma_prob

    def prob_normal_distribution(self, a, b):
        '''
        Computes the probability of a value given a variance for a normal distribution
        a - value argument
        b - zero centered variance
        '''
        return 1 / np.sqrt(2 * np.pi * b) * np.exp(-(a**2/(2*b)))

    def prob_triangular_distribution(a , b):
        '''
        Computes the probability of a value given a variance for a triangular distribution
        a - value argument
        b - zero centered variance
        '''
        if np.abs(a) >  np.sqrt(6 * b):
            return 0
        else:
            return (np.sqrt(6*b) - np.abs(a)) / (6 * a)

    def sample_motion_model_velocity(self, pose, command, n, d_time):
        #TODO: test model with higher dimension motion, currently only [x, y, theta] and [v, w] motion is supported 
        _v, _w = command 
        _x, _y, _theta = pose.T
        
        # generate command samples using motion uncertainties
        v_hat = np.random.normal(loc=0, scale=self._a_1 * np.abs(_v) + self._a_2 * np.abs(_w), size=(len(_x), n)) + _v
        w_hat = np.random.normal(loc=0, scale=self._a_3 * np.abs(_v) + self._a_4 * np.abs(_w), size=(len(_x), n)) + _w
        gamma_hat = np.random.normal(loc=0, scale=self._a_5 * np.abs(_v) + self._a_6 * np.abs(_w), size=(len(_x), n))
                
        x = _x - np.divide(v_hat, w_hat).T * np.sin(_theta) + np.divide(v_hat, w_hat).T * np.sin((w_hat * d_time).T + _theta)
        y = _y + np.divide(v_hat, w_hat).T * np.cos(_theta) - np.divide(v_hat, w_hat).T * np.cos((w_hat * d_time).T + _theta)
        theta = (_theta + (w_hat * d_time + gamma_hat * d_time).T)
       
        return np.concatenate(([x.flatten()],[y.flatten()],[theta.flatten()]),axis=0).T


class VelocityMotionModel:

    step_particles = np.array([])

    def __init__(self, alphas, pose, sample_size=10):
        self.vmm = VMMGenerator(alphas) 
        self.sample_size = sample_size
        self.step_particles = [pose]

    def update(self, command, d_time):
        if(len(self.step_particles) == 1):            
            particle_update = self.vmm.sample_motion_model_velocity(self.step_particles[-1], command, n=self.sample_size, d_time=d_time)
        else:
            particle_update = self.vmm.sample_motion_model_velocity(self.step_particles[-1], command, n=1, d_time=d_time)
        self.step_particles.append(particle_update)
    
    def graph(self):
        
        for step in self.step_particles:
            plt.plot(step.T[0], step.T[1], 'o', markerfacecolor='white')
        plt.show()
            

if __name__ == "__main__":
    print ("Executing __main__ method for the VMM class")
    alphas = np.array([0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
    initial_pose = np.array([[1,0,np.pi/2]])
    particles = 100
    iterations = 150
    command = [np.pi, np.pi/100]
    print ("Using alpha values: " + ' '.join(map(str, alphas)))    
    print("Using initial pose: " + ' '.join(map(str, initial_pose)))
    print("Samples used: " + particles.__str__())
    print("Movement steps: " + iterations.__str__())
    print("Using command : " + ' '.join(map(str, command)))

    vmm = VMMGenerator(alphas)    

    plt.plot(initial_pose.T[0], initial_pose.T[1], 'o', markerfacecolor='black')
    step_particles = vmm.sample_motion_model_velocity(initial_pose, command, n=particles, d_time=1)

    plt.plot(step_particles.T[0], step_particles.T[1], 'o', markerfacecolor='white')
    for step in range(0,iterations):
        step_particles = vmm.sample_motion_model_velocity(step_particles, command, n=1, d_time=1)
        plt.plot(step_particles.T[0], step_particles.T[1], 'o', markerfacecolor='white')

    plt.show()