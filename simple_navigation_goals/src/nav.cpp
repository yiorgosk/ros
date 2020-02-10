#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <iostream>
#include <utility>
#include <vector>



typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

int main(int argc, char **argv)
{
    ros::init(argc,argv,"nav_");

    MoveBaseClient action_client("move_base",true);

    while(!action_client.waitForServer(ros::Duration(5.0)))
        ROS_INFO("Waiting for Server!");

    while(ros::ok())
    {
        float x,y;
        int n=0;
        std::cout<<"Enter the number of points you want your robot to move "<<std::endl;
        std::cin>>n;
        std::vector < std::pair <float, float> > points;

        for(int i=0;i<n;i++)
        {
            std::cout<<"Enter value for point x "; std::cin>>x;
            std::cout<<"\nEnter value for point y "; std::cin>>y;
            points.push_back( std::make_pair(x,y) );
        }

        for(int j=0;j<n;j++)
        {
            move_base_msgs::MoveBaseGoal goal;

            goal.target_pose.header.frame_id="base_link";
            goal.target_pose.header.stamp=ros::Time::now();
            goal.target_pose.pose.position.x=points[j].first;
            goal.target_pose.pose.position.y=points[j].second;
            goal.target_pose.pose.orientation.w=1.0;

            ROS_INFO("Sending Goal");
            action_client.sendGoal(goal);

            action_client.waitForResult();

            if(action_client.getState()==actionlib::SimpleClientGoalState::SUCCEEDED)
                ROS_INFO("The Goal Was Succeesful!");
            else
                ROS_INFO("The Goal Was Unsucceesful!");
        }
    }

    return 0;
}
