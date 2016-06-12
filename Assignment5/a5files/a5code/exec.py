execfile("StrokeHmm.py") #only needed in the separate file
a = HMM(["sunny", "cloudy", "rainy"], ["ob"], {"ob": 1}, {"ob": 4 })
a.priors = {"sunny":0.63, "cloudy": 0.17, "rainy": 0.2}
a.transitions = {"sunny":{"sunny":0.5, "cloudy":0.375, "rainy":0.125},
               "cloudy":{"sunny": 0.25, "cloudy": 0.125, "rainy":0.675},
               "rainy":{"sunny":0.25, "cloudy":0.375, "rainy":0.375}}
a.emissions = {"sunny":{"ob":[0.6, 0.2, 0.15, 0.05]},
              "cloudy":{"ob":[0.25, 0.25, 0.25, 0.25]},
              "rainy":{"ob":[0.05, 0.1, 0.35, 0.5]}}
print a.label([{"ob":0},{"ob":2},{"ob":3}])
