
from instagramy import InstagramUser as IU  

# givenUN = input("Enter a valid and existing Instagram's user name: ")  

unInstance = IU('javax00')  

followingNumber = unInstance.number_of_followings  

print('The total number of followings from the given user name by you is:', followingNumber)  