# Copyright 2020-2022 OpenDR European Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# MIT License
#
# Copyright (c) 2021 Halil Ibrahim Ugurlu
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String
from cv_bridge import CvBridge


class range_image_node():

    def __init__(self):
        rospy.init_node('listener', anonymous=True)
        self.r = rospy.Rate(10)
        self.raw_image_pub = rospy.Publisher('range_image_raw', Float32MultiArray, queue_size=10)
        rospy.Subscriber("/model_name", String, self.model_name_callback)
        self.r.sleep()
        rospy.Subscriber("/" + self.model_name + "/range_finder/range_image", Image, self.range_callback)
        rospy.spin()

    def range_callback(self, data):
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(data)
        arr = Float32MultiArray()
        arr.data = list(cv_image.reshape(4096))
        self.raw_image_pub.publish(arr)

    def model_name_callback(self, data):
        self.model_name = data.data


node_class = range_image_node()
