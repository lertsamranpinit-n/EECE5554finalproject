%1 is Yaw, 2 is pitch, 3 is roll, 4 is time, 5 is size
function a = loadData(name)
    bag = rosbag(name);
    imuSel = select(bag,'Topic','/imu');
    msgs = readMessages(imuSel,"DataFormat","struct");
    s = imuSel.NumMessages;
    
    time_offset = double(msgs{1}.Header.Stamp.Sec) + double(msgs{1}.Header.Stamp.Nsec)*10^-9;
    
    for m=1:s
        time_tmp = double(msgs{m}.Header.Stamp.Sec) + double(msgs{m}.Header.Stamp.Nsec)*10^-9;
        time(m) = time_tmp - time_offset;
    
        str = split(msgs{m}.VNYMR, ',');
        yaw(m) = deg2rad(str2double(str(2)));
        pitch(m) = deg2rad(str2double(str(3)));
        roll(m) = deg2rad(str2double(str(4)));
    end

    yaw = unwrap(yaw);
    pitch = unwrap(pitch);
    roll = unwrap(roll);

    yaw = rad2deg(yaw);
    pitch = rad2deg(pitch);
    roll = rad2deg(roll);

    a = yaw;
    a(2,:) = pitch;
    a(3,:) = roll;
    a(4,:) = time;
    a(5,1) = s;
end