clear;
curr = loadData('Jason_flexion.bag');
s = curr(5,1);
yaw = curr(1,:);
pitch = curr(2,:);
roll = curr(3,:);
time = curr(4,:);

%zero from starting position
yaw = yaw - yaw(1);
pitch = pitch - pitch(1);
roll = roll - roll(1);

%adjustement
adjYaw = lowpass(yaw,.001);
adjPitch = lowpass(pitch,.001);
adjRoll = lowpass(roll,.001);

mainAxis = adjPitch;
secondaryAxis1 = adjYaw;
secondaryAxis2 = adjRoll;
cal = .009;
scanDist = 1;
threshold = -.03;

t = findTransitions(mainAxis, time, s, cal, scanDist);
xPoints = t{1};
yPoints = t{2};

%{
minMax = findMinMax(mainAxis, time, s, cal, scanDist, threshold);
minTime = minMax{1,1};
maxTime = minMax{2,1};
minIndex = minMax{1,2};
maxIndex = minMax{2,2};

for m=1:length(maxIndex)
    maxI = maxIndex(m);
    minI = minIndex(m);
    mainAxisTravel(m) = mainAxis(maxI) - mainAxis(minI);
    secondaryMax = atan(sqrt(tan(secondaryAxis1(maxI))^2 + tan(secondaryAxis2(maxI))^2));
    secondaryMin = atan(sqrt(tan(secondaryAxis1(minI))^2 + tan(secondaryAxis2(minI))^2));
    secondaryAxisTravel(m) = abs(secondaryMax - secondaryMin);
end
%}

hold on
plot(time, adjYaw, 'r');
plot(time, adjPitch, 'black');
plot(time, adjRoll, 'b');
%scatter(xPoints, yPoints,'gO');
%xline(minTime);
%xline(maxTime);
hold off
legend('yaw','pitch','roll');
xlabel("Time (s)");
ylabel("Angle (degrees)");
