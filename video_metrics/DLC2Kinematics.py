#Import the library DLC2Kinematics 
import dlc2kinematics

#Import pickle and pandas
import pickle
import pandas as pd

#Import data to use. Path should lead to the h5 file!
df, bodyparts, scorer = dlc2kinematics.load_data("C:\\Users\\Admin\\Desktop\\DLC2Kin\\45137_RB_W03VideoProcessed2021-12-21T11_20_37DLC_resnet50_Dystonia_TestApr21shuffle1_500000.h5")

# Compute Velocity

# For one or few bodyparts. Write the name of the bodypart inside the ['']
df_vel_perbodypart = dlc2kinematics.compute_velocity(df,bodyparts=['nose','tailbase', 'left_hindlimb_heel', 'right_hindlimbheel'])
#For all bodyparts
df_vel_allbodyparts = dlc2kinematics.compute_velocity(df,bodyparts=['all'])
# Store velocity in pickle file
df_vel_perbodypart.to_pickle('C:\\Users\\Admin\\Desktop\\DLC2Kin\\vel_perbodypart.pkl', compression='infer', protocol=5, storage_options=None)
df_vel_allbodyparts.to_pickle('C:\\Users\\Admin\\Desktop\\DLC2Kin\\vel_allbodyparts.pkl', compression='infer', protocol=5, storage_options=None)

# Read the dataframe
#velocitydatabase=pd.read_pickle(r'C:\Users\Admin\Desktop\DLC2Kin\velocity.pkl', compression='infer', storage_options=None)
#velocitydatabase.columns

#Compute Acceleration
#For all bodyparts
df_acc_allbodyparts = dlc2kinematics.compute_acceleration(df,bodyparts=['all'])
#For only few bodyparts - replace what is in [] with the name of the parts you want
df_acc_perbodyparts = dlc2kinematics.compute_acceleration(df,bodyparts=['nose','tailbase', 'left_hindlimb_heel', 'right_hindlimbheel'])

#Compute Speed
df_speed = dlc2kinematics.compute_speed(df,bodyparts=['nose','tailbase', 'left_hindlimb_heel', 'right_hindlimbheel'])

#Store the speed in a pickel file
df_speed_perbodypart.to_pickle('C:\\Users\\Admin\\Desktop\\DLC2Kin\\speed.pkl', compression='infer', protocol=5, storage_options=None)

#Computations for joint coordinates

#To compute joint angles, we first create a dictionary where keys are the joint angles and the corresponding values are the set of bodyparts. Replace the names inside [] for your parts
joints_dict= {}
joints_dict['Standing_angle']  = ['tailbase', 'left_hindlimb_heel', 'right_hindlimbheel']
# Compute joint angles
joint_angles = dlc2kinematics.compute_joint_angles(df,joints_dict)
# Joint angular velocity
joint_vel = dlc2kinematics.compute_joint_velocity(joint_angles)
# Joint angular acceleration
joint_acc = dlc2kinematics.compute_joint_acceleration(joint_angles)
# Compute correlation of angular velocity
corr = dlc2kinematics.compute_correlation(joint_vel, plot=True)
# Compute PCA of angular velocity
pca = dlc2kinematics.compute_pca(joint_vel, plot=True)

#PCA-based reconstruction of postures
dlc2kinematics.plot_3d_pca_reconstruction(df_vel, n_components=10, framenumber=500,
bodyparts2plot= bodyparts2plot, bp_to_connect= bp_to_connect)

 # UMAP (Uniform Manifold Approximation and Projection for Dimension Reduction) Embeddings
embedding, transformed_data = dlc2kinematics.compute_umap(df, key=['LeftForelimb', 'RightForelimb'], chunk_length=30, fit_transform=True, n_neighbors=30, n_components=3,metric="euclidean")
dlc2kinematics.plot_umap(transformed_data, size=5, alpha=1, color="indigo", figsize=(10, 6))