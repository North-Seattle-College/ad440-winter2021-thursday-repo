import {TestUserIdUI} from "../ui/ui-test-user-id.js";

(async () => {
    // create time array
    const timeArray = []
    let i;
    
    (() => {
        for (i = 0; i < 40; i++) {
        // start timer
        let startTime = getTime();
        TestUserIdUI()
            .then((e) => {
                let endTime = getTime();
                milliseconds = endTime - startTime;
                timeArray[i] = milliseconds
            })
    }}).then((e) => {
        let totalTime = 0;
        for (time in timeArray) {
            totalTime += time;
        }
        avgTime = totalTime/40;
        console.log(`Total time: ${totalTime}`)
        console.log(`Average time: ${avgTime}`)
    })
})