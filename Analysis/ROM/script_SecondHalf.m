clear;
curr = loadData('Note_flexion.bag');
% 150 offset for June
offset = 20;

s = curr(5,1);
sRound = round(s/2);
yaw = curr(1,sRound+offset:s);
pitch = curr(2,sRound+offset:s);
roll = curr(3,sRound+offset:s);
time = curr(4,1:sRound-offset);

%zero from starting position
yaw = yaw - yaw(1);
pitch = pitch - pitch(1);
roll = roll - roll(1);

%adjustement
adjYaw = detrend(lowpass(yaw,.001));
adjPitch = detrend(lowpass(pitch,.001));
adjRoll = detrend(lowpass(roll,.001));

%zero from starting position
adjYaw = adjYaw - adjYaw(1);
adjPitch = adjPitch - adjPitch(1);
adjRoll = adjRoll - adjRoll(1);

mainAxis = adjPitch;
secondaryAxis1 = deg2rad(adjYaw);
secondaryAxis2 = deg2rad(adjRoll);
cal = .3;
scanDist = 1;
threshold = 7;

t = findTransitions(mainAxis, time, sRound - offset, cal, scanDist);
xPoints = t{1};
yPoints = t{2};

%%{
minMax = findMinMax(mainAxis, time, sRound - offset, cal, scanDist, threshold);
minTime = minMax{1,1};
maxTime = minMax{2,1};
minIndex = minMax{1,2};
maxIndex = minMax{2,2};

%{
minTime(3) = [];
minIndex(3) = [];
%}

if length(maxIndex) > length(minIndex)
    l = length(minIndex);
else
    l = length(maxIndex);
end

for m=1:l
    maxI = maxIndex(m);
    minI = minIndex(m);
    mainAxisTravel(m) = mainAxis(maxI) - mainAxis(minI)
    secondaryMax = atan(sqrt(tan(secondaryAxis1(maxI))^2 + tan(secondaryAxis2(maxI))^2));
    secondaryMin = atan(sqrt(tan(secondaryAxis1(minI))^2 + tan(secondaryAxis2(minI))^2));
    secondaryAxisTravel(m) = rad2deg(abs(secondaryMax - secondaryMin))
end
%}

hold on
plot(time, adjYaw, 'r');
plot(time, adjPitch, 'black');
plot(time, adjRoll, 'b');
scatter(xPoints, yPoints,'gO');
xline(minTime);
xline(maxTime);
hold off
legend('yaw','pitch','roll');
xlabel("Time (s)");
ylabel("Angle (degrees)");
