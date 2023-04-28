clear;
curr = loadData('Note_flexion.bag');
s = curr(5,1);
s = round(s/2);
yaw = curr(1,1:s);
pitch = curr(2,1:s);
roll = curr(3,1:s);
time = curr(4,1:s);

%zero from starting position
yaw = yaw - yaw(1);
pitch = pitch - pitch(1);
roll = roll - roll(1);

%adjustement
adjYaw = lowpass(yaw,.001);
adjPitch = lowpass(pitch,.001);
adjRoll = lowpass(roll,.001);

%shift to the right
shift = 20;
time = [time(1:s) time(s)+time(1:shift)];
adjYawInt = zeros(1,shift) + adjYaw(1);
adjYaw = [adjYawInt adjYaw(1:s)];

adjPitchInt = zeros(1,shift) + adjPitch(1);
adjPitch = [adjPitchInt adjPitch(1:s)];

adjRollInt = zeros(1,shift) + adjRoll(1);
adjRoll = [adjRollInt adjRoll(1:s)];

mainAxis = adjPitch;
secondaryAxis1 = deg2rad(adjYaw);
secondaryAxis2 = deg2rad(adjRoll);
cal = .5;
scanDist = 1;
threshold = 6;

t = findTransitions(mainAxis, time, s, cal, scanDist);
xPoints = t{1};
yPoints = t{2};

%%{
minMax = findMinMax(mainAxis, time, s, cal, scanDist, threshold);
minTime = minMax{1,1};
maxTime = minMax{2,1};
minIndex = minMax{1,2};
maxIndex = minMax{2,2};

%{
minTime(3) = [];
minIndex(3) = [];
%}

for m=1:length(maxIndex)
    maxI = maxIndex(m);
    minI = minIndex(m);
    mainAxisTravel(m) = mainAxis(maxI) - mainAxis(minI);
    secondaryMax = atan(sqrt(tan(secondaryAxis1(maxI))^2 + tan(secondaryAxis2(maxI))^2));
    secondaryMin = atan(sqrt(tan(secondaryAxis1(minI))^2 + tan(secondaryAxis2(minI))^2));
    secondaryAxisTravel(m) = rad2deg(abs(secondaryMax - secondaryMin));
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
