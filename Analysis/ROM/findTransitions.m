%row: 1->xPoints, 2->yPoints
function cell = findTransitions(axis, time, s, cal, scanDist)
    cnt = 1;
    for m=1+scanDist:scanDist:s
        mag = abs(axis(m) - axis(m-scanDist));
        if mag > cal
            xPoints(cnt) = time(m);
            yPoints(cnt) = axis(m);
        else
            xPoints(cnt) = 0;
            yPoints(cnt) = 0;
        end
        cnt = cnt + 1;
    end
    cell = {xPoints; yPoints};
end