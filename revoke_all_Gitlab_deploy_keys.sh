#!/bin/bash
echo "Please Insert your private Token: "
read token
echo "Please Insert Number of Projects (can be extracted form the gui): "
read total_proj
for proj_num in `seq 1 $total_proj`;
        do
                for key_id in `curl -s -H "PRIVATE-TOKEN: $token" "https://gitlab.server.com/api/v3/projects/$proj_num/keys/" --insecure | grep -o -P '.{0,0}id.{0,4}' | cut -d: -f2`;
                        do
                                curl -s -X DELETE -H "PRIVATE-TOKEN: $token" "https://gitlab.server.com/api/v3/projects/$proj_num/keys/$key_id/" --insecure;
                        done
        done
