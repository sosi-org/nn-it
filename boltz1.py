import numpy as np
#print help(np.floor)
#print dir(np.zeros((1,1)))
#exit()

VERBOSE = True

#removes correaltions
class DistrInterface(object):
    """ Measures and mimics correlation ininput data"""
    def energy(self, state):
        pass

    def sample(self):
        #sample freely, no input condisioned (clamped)
        pass

    def sample_input(self, x):
        #sample given input
        pass

    def marginal_input(self, x):
        #marginal given input
        pass

    def get_dual(self):
        return self.dual
#
    def sample_correlation(self):
        """ Used for training"""
        pass

class Boltzmann1(DistrInterface):
    def __init__():
        self.W = np.eye()

    def energy(self, state):
        pass

class RBoltzmann1(DistrInterface):
    def get_dual(self):
        return self.dual
    def energy(self, state):
        (v, h) = state
        pass

class BinaryDataProvider(object):
    def get_raw_sample(self, i):
        return None

    def samples(self):
        return 0

    def get_next_sample(self):
        yield None

    def shuffle(self):
        """ prepare for next shuffled"""
        pass

    def get_next_shuffled(self):
        pass

    def set_mode(self, mode):
        assert mode in ['train', 'test', 'validation']

    def format(self, sample_vector):
        pass

#http://deeplearning.net/datasets/
#class test_

class MNISTLoader(BinaryDataProvider):
    preloaded = False
    @staticmethod
    def preload(path):
        import os
        #path = '/home/sohail/ml/datasets/mnist'
        absolute_filename = os.path.join(path, 'mnist.pkl.gz')

        if VERBOSE:
            print 'loading MNIST', ;flush_stdout()
        # Loading code from: http://deeplearning.net/tutorial/gettingstarted.html
        import cPickle, gzip, numpy
        f = gzip.open(absolute_filename, 'rb')
        train_set, valid_set, test_set = cPickle.load(f)
        f.close()
        if VERBOSE:
            print 'done.' ;flush_stdout()

        MNISTLoader.train_set, MNISTLoader.valid_set, MNISTLoader.test_set = train_set, valid_set, test_set

    def __init__(self, mode='train'):
        if not MNISTLoader.preloaded:
            # Downloaded from http://deeplearning.net/data/mnist/mnist.pkl.gz
            MNISTLoader.preload('/home/sohail/ml/datasets/mnist')
            MNISTLoader.preloaded = True
        self.set_mode(mode)

    def set_mode(self, mode):
        assert mode in ['train', 'test', 'validation']
        mode__dset_lookup = {'train': 0, 'test': 1, 'validation': 2}
        datasets = [MNISTLoader.train_set, MNISTLoader.valid_set, MNISTLoader.test_set]
        self.active_dataset = datasets[mode__dset_lookup[mode]]
        if VERBOSE:
            print 'active dataset: \'%s\''%(mode,)

    def format(self, sample_vector):
        return sample_vector.reshape(28, 28)

    def format_text(self, sample_vector):
        return sample_vector.reshape(28, 28)

    def get_raw_sample(self, i):
        vector = self.active_dataset[0][i]
        label = self.active_dataset[1][i]
        return vector, label

    def get_full_data(self):
        vects = self.active_dataset[0]
        labels = self.active_dataset[0]
        return (vects, labels)

def flush_stdout():
    import sys
    sys.stdout.flush()


def print_image_28x28(image):
    #exit()
    w = 28
    for y in range(784/w):
        for x in range(w):
            print '.' if image[x+w*y] < 0.5 else '1',
        print
    print

def test_mnist():
    #print 'loading', ;flush_stdout()
    d = MNISTLoader()
    #print 'done.' ;flush_stdout()
    print d
    print type(d.train_set)
    print len(d.train_set)
    print d.train_set

    print d.train_set[0].shape #(50000, 784)
    print d.train_set[1].shape #(50000,) of int64  #labels

    print d.train_set[1][0]
    print type(d.train_set[1][0])  # int64

    print d.train_set[0][0,0]
    print type(d.train_set[0][0,0])  # float32



    for t in [MNISTLoader.train_set, MNISTLoader.valid_set, MNISTLoader.test_set]:
        print t[1].shape,  #labels
        print t[0].shape,  #data
        print type(t[1][0]),  # int64
        print type(t[0][0,0])  # float32
        #(50000,) (50000, 784) <type 'numpy.int64'> <type 'numpy.float32'>
        #(10000,) (10000, 784) <type 'numpy.int64'> <type 'numpy.float32'>
        #(10000,) (10000, 784) <type 'numpy.int64'> <type 'numpy.float32'>


        vector = t[0]
        print (np.min(vector), np.max(vector)),  #(0,0.996)
        i = 100
        image = vector[i]
        print_image_28x28(image)
        
        #matrix = image.reshape(28, 28)
        #print np.floor(matrix*10).astype(int)

def factorize():    
        print 7.*8.*7.*2
        m = 784./7./8./7./2.
        print m, ":",
        for i in range(2, int(m**0.5)):
            if float(m)/float(i) % 1. == 0.:
                print i,
        print  # 2 4 7 8 14 16

import matplotlib.pyplot as plt

def show_image(matrix, show=True):
    plt.imshow(matrix, cmap='bone')
    if show:
        plt.show()
    #plt.hist( np.log10(ea+leps), 150)

def show_images(matrix_list, grid_shape=None):
    if grid_shape is None:
        n = len(matrix_list)
        w = int((n-0.000001)**(0.5) + 1)
        h = int((n-.00000001)/w) + 1
        print w, h
    grid_shape = (w, h)

    i = 0
    for vector in matrix_list:
        matrix = vector.reshape(28, 28)
        plt.subplot(w, h, i+1)
        plt.imshow(matrix, cmap='bone')
        i+=1
    plt.show()

def load_autocorrel_demo():
    d = MNISTLoader('test')
    vec, label = d.get_raw_sample(100)
    #print vec
    print "label=", label
    #print d.format((vec*10).astype(int))
    print_image_28x28(vec)
    vects, labels = d.get_full_data()
    vects = (vects > 0.5)*1.
    print vects.shape
    sample_size, n = vects.shape
    #vects.shape = 
    print "calculating autocorrel-",;flush_stdout()
    autocorr = np.dot(vects[:100, :].T, vects[:100, :])
    print "lation"; flush_stdout()
    print autocorr[::20, ::20].shape
    print np.sum(np.fabs(autocorr)/(autocorr.size*1.))  #average: 1.5 ! what?
    #print autocorr.size
    print np.sum(np.fabs(autocorr)>1.)/(autocorr.size*1.)
    #show_image(autocorr)

    ac4d = autocorr.reshape(28,28, 28,28)
    ac4d_i = np.swapaxes(ac4d, 1, 2)
    print ac4d.shape
    #show_image(ac4d_i[:,:,10,10]) # rows versus rows, cols=10,10
    show_image(ac4d_i[10, 10, :, :])
        #shows some pattern.
        #There is some continuity here.
        #Also 'some' continuity along all 4 dimensions here!
    #help(np.swapaxes)

    #Why nothing for sampling?

def sampling_demo():
    n = 28*28
    n1 = n+1
    W = np.eye(n1, n1)
    v = np.random.rand(n)
    v1 = np.hstack((v, 1.))
    print v.shape, v1.shape 
    energy = np.dot(np.dot(v1, W), v1)  #W=I => indep. => energy=v^2=|v|.
    # Each independent feature adds to energy.
    print energy
    #activation = activity of one, when all others (Except for that) are given (and condisioned).
    def ewnergy1(v):
        v1 = np.hstack((v, 1.))
        print v.shape, v1.shape 
        energy = np.dot(np.dot(v1, W), v1)  #W=I => indep. => energy=v^2=|v|.

    for i in range(100):
        v = np.random.rand(n)
        e = energy1(v)
        #incomplete

class I28x28:
    @staticmethod
    def shift(v, xshift, yshift, background=0.):
        matrix = v.reshape(28, 28).copy() #necessary
        #print np.median(matrix)
        #matrix[xshift:, yshift:] = matrix[:-1-xshift:, :-1-yshift]
        assert int(xshift) == xshift
        assert int(yshift) == yshift
        assert int(xshift) == xshift
        assert int(yshift) == yshift

        if xshift > 0:
            matrix[xshift:, :] = matrix[:-xshift, :]
            matrix[:xshift, :] = background
        elif xshift < 0:
            matrix[:-xshift, :] = matrix[xshift:, :]
            matrix[-xshift:, :] = background
        else:
            pass
        if yshift > 0:
            matrix[:, yshift:] = matrix[:, :-yshift]
            matrix[:, :yshift] = background
        elif yshift < 0:
            matrix[:, :-yshift] = matrix[:, yshift:]
            matrix[:, -yshift:] = background
        else:
            pass

        return matrix.reshape(28*28)

def naive_gauss_reproduce_demo():
    d = MNISTLoader('test')
    vects, labels = d.get_full_data()
    #ndim = vects.shape[1]
    vects = (vects > 0.5)*1.
    sample_size, ndim = vects.shape
    #num_samples_taken_into_account = 1000
    #v_sub = vects[:num_samples_taken_into_account, :]
    #REDUCE the number of samples
    v_sub = vects[::1, :]; sample_size = v_sub.shape[1]
    mu = np.mean(v_sub, axis=0)  # * 0.
    mu_scalar=np.mean(mu.ravel())  #scalar
    mu_scalar = float(mu_scalar)
    mu = mu * 0 + mu_scalar
    #mu = mu * 0


    if False:
      for si in range(v_sub.shape[0]):
        #v_sub[si] = v_sub[si] - mean(v_sub[i])
        #dx, dy = np.random.randint(-15,15), np.random.randint(-15,15)  #too scrambled
        dx, dy = np.random.randint(-15,15), np.random.randint(-15,15)  #too scrambled
        v_sub[si] = I28x28.shift(v_sub[si], dx,dy, background=0)
        if False:
            v_sub[si] = v_sub[si] - mu
            i1 = v_sub[si].copy()
            v_sub[si] = I28x28.shift(v_sub[si], 0, 15, background=0)
            i2 = v_sub[si].copy()
            v_sub[si] = I28x28.shift(i1, 0, -15, background=0)
            i3 = v_sub[si].copy()
            v_sub[si] = I28x28.shift(i1, -15, -15, background=0)
            i4 = v_sub[si].copy()
            show_images([i1, i2, i3, i4])
        if (si+1) % 100 == 1:
            print "si:%d      \r"%(si,),

    print "calculating autocorrelation",;flush_stdout()
    autocorr = np.dot(v_sub.T, v_sub) / float(sample_size) * 0.0001
    print "."; flush_stdout()
    print autocorr.shape
    cov = autocorr
    #fixme: How come is it NOT positive-semidifinite?
    #mu = np.sum(v_sub, axis=0)
    ilist = []
    for i in range(16):
        #Works, but why the mean should not be subtracted?
        alpha = 1
        s = np.random.multivariate_normal(mu, cov*alpha+(1.-alpha)*np.eye(ndim))
        #s = mu
        ilist.append(s)
        #s28x28 = s.reshape(28, 28)
        #show_image(s28x28, show=False)
    #plt.show()
    show_images(ilist)
    #Problem: 3 is too dominant
    #Mean/covar bug fixed. Now makes sense in terms of classic mean/covariance.

if __name__ == '__main__':
    #test_mnist()
    #factorize()
    #load_autocorrel_demo()
    #sampling_demo()

    #Has a form similar to Gaussian. Exp(vWv)
    #It is simply a Gaussian, but on (0,1). Damn. (So it is basically Genz)
    #My intuition for normalizing Genz was good: Use the lieanr transformation, but not to make it uniform. (how?)
    #Learning:   W != correl, because we also have a Z. The balance in between that and Z. (only because it's {0,1})
    #Boltzmann Machine is simple? As if it's a simpel Gaussian correlation-detector. Which is tained online.
    #So, yes, do think of it like a Gaussian.
    #Also see Laplace's method, page 341 of 1st edition (D.McKay). He assumed normalisation factor does not exist from beginning. (And it's Taylor)
    #Can we make Z easier by the transforamtion?
    #So can we reproduce the original samples using the correlation matrix?
    #It is intersting that in Gaussian, mue can be inside W.

#fastCopyAndTranspose?

    #Now let's generate some Gaussian.
    #The autocorrelation is so tighting from all directions that can determine everything!
    #Let's try: naive_gauss_reproduce()
    naive_gauss_reproduce_demo()
    #In Genz, integration is rndom genration (sampling).

    # A Bernouli version of Gaussian?

    #..
    #We limit information by choosing Bernouli {0,1}.

    #Restricted BM is another idea.
    #It can be seen as just adding dimensions. But what about preserving infomration between V, H?

    #A way to increase capacity is to add extra variables (hidden).
    #But what will this mean in terms of RBM/multiple layers? (remember: they could be arbitrary). It is attaching them to another Gaussian. So it keeps reducing dimensions untill it "closes" the distribution (by specifyint all dimensions).
    #Problem: Combining two Gaussians is Gaussian. To increasing dimensions is useful, but attaching them to another Gaussian is useless. It gives the problem to another external machine to solve. But it would need a nonlinearity.

    #Adding the mean in sampling, means we add a white '3'. Which means the raw samples have a hole in '3' otherwise.

    #Howdo we improve this? More samples? No, not enough.

    #But people already have used Eigenfaces. They probably have tries sampling from that space too.
    #And the results now do look like eigenfaces (e.g. DC comonent in back). Back to Gaussian: how can we force eigenfaces to do differently.
    #But that's PCA/dim-reduction. 
    #Yes: Gaussian does reduce the dimenions, but it is not easy to see the reduces dimensiones. But they still obey the eigenvectors. The eigenvectors encode the correaltions. But not explicitly. PCA makes them explicit.
    #The PCA/RBM => explicitly extract that space: Some Q where  vAv = vQBQv

    #What would 'sampling' (as in PatternTheory) mean in a PCA/Eigenface mindset?
    #We kind of reduce the dimensions and then reproduce it. But it's still not the sampling idea.

    #What RBM adds is notin of marginalisation and condisioning (clamping)
    #Marginalising = Activity function. (but plus Expected value?)
    #Activity is also population-marginalisation.

    #Why is it not smooth anymore?

    #We need to inject an external distribution. That is, H distribution in RBM.
    #But in MLP, it is the output. In PT (Pattern Theory/sampling approach), it is [generated?].

    #BTW, Where is the nonlinearity (of MLP)?

    #In Gaussian, crrelation is between pairs only. In one-layer [R]BM, too.

    #Observation: When I generate more samples, they all subjectively look similar. First guess, they all use a uniform distribution on the other side of the Gaussian. (Although we dont have hidden units, but we can see this as hidden units that have a purely Gasussian distribution).
    #So, it just does a dim-reduction.
    #=> Hence, The next step is to do an actual PCA.
    #Hinton also compared it to PCA. Because it is really comparable to PCA. IT chooses the dimensions automatically. (Can it put weight on H dimentions?)

    #(reminder) Output of RBM is between two Qs in vAv=vQhhQv. (minimizing vQh, and vQh->(Q^T)->v) However, PCA is also about breaking down A into QQ.
    #What is added to RBM that makes it different to this PCA (Q)?

    #Note, they dont look like the original because I just did sampling.

    #The criterion for learning is to reproduce the input. But from what. From its map. But a map of course makes it. The map should reduce it really.
    #So a Gaussian extention is a Linear trnaformation that is most faithful to input when the dimensions are Reduced: A PCA which those few dimensions is chosen based on this criterion. (But still the nonlinearity is has not entered.)
    #Older Note: note that normalisation is key (implicitly used in Boltzmann's formalism as temperature).
    #Brain's temperature: Neormalisation/[Audio-engineering's sense of]Compression.

    #So we dont even reproduce  the distribution! The only criterion is reproducing it. (How dow it bring non-linearity?)
