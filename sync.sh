aws s3 sync out s3://fmb-aws-bucket/KatasterKI/scenes/ --exclude "*"  --include "*.jpg"
aws s3 cp out/KatasterKI_scene_list.csv s3://fmb-aws-bucket/Data/KatasterKI_scene_list.csv