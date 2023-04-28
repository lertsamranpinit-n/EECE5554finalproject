%cell = {minTime, minIndex; maxTime, maxIndex}
function cell = findMinMax(axis, time, s, cal, scanDist, threshold)
    t = findTransitions(axis, time, s, cal, scanDist);
    xPoints = t{1};
    
    cnt1=1;
    cnt2=1;
    for m=2:length(xPoints)
        if (xPoints(m-1)==0 && xPoints(m)~=0) 
            leftLimits(cnt1) = xPoints(m);
            leftLimit(cnt1) = m;
            cnt1 = cnt1+1;
        end
        if (xPoints(m-1)~=0 && xPoints(m)==0) 
            rightLimits(cnt2) = xPoints(m-1);
            rightLimit(cnt2) = m-1;
            cnt2 = cnt2+1;
        end
    end
    
    % determine min / max
    minCnt = 1;
    maxCnt = 1;
    for m=1:length(leftLimit)
        if m==1
            x1 = 1;
        else
            x1 = rightLimit(m-1);
        end
        x2 = leftLimit(m);

        [maxV, maxI] = max(axis(x1:x2));
        [minV, minI] = min(axis(x1:x2));

        if maxV > threshold
            maxIndex(maxCnt) = maxI + x1;
            maxTime(maxCnt) = time(maxIndex(maxCnt));
            maxCnt = maxCnt + 1;
        elseif minV < threshold
            minIndex(minCnt) = minI + x1; % x1 - 1
            minTime(minCnt) = time(minIndex(minCnt));
            minCnt = minCnt + 1;
        end
    end

    cell = {minTime, minIndex; maxTime, maxIndex};
end