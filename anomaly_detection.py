import math

def mean(values):
    return sum(values) / len(values)

def variance(values):
    m = mean(values)
    return mean([(x - m) ** 2 for x in values])

def light_curve_anomaly(light_curve):
    baseline = sorted(light_curve)[len(light_curve) // 2]
    deviation = mean([abs(x - baseline) for x in light_curve])
    return deviation / baseline

def motion_anomaly(positions):
    velocities = []
    for i in range(len(positions) - 1):
        velocities.append([
            positions[i+1][j] - positions[i][j]
            for j in range(3)
        ])

    accelerations = []
    for i in range(len(velocities) - 1):
        accelerations.append([
            velocities[i+1][j] - velocities[i][j]
            for j in range(3)
        ])

    mags = [
        math.sqrt(sum(a[j] ** 2 for j in range(3)))
        for a in accelerations
    ]
    return mean(mags)

def debris_scatter_anomaly(debris_vectors):
    dispersions = []
    for i in range(3):
        dispersions.append(
            variance([v[i] for v in debris_vectors])
        )
    return math.sqrt(sum(d ** 2 for d in dispersions))

def gamma_anomaly(spectrum, target_energy=511):
    closest = min(
        spectrum,
        key=lambda x: abs(x[0] - target_energy)
    )
    return closest[1]

def classical_anomaly_score(data):
    return (
        light_curve_anomaly(data["light"]) +
        motion_anomaly(data["positions"]) +
        debris_scatter_anomaly(data["debris"]) +
        gamma_anomaly(data["gamma"])
    )

if __name__ == "__main__":
    test_data = {
        "light": [1.0, 0.98, 1.01, 0.97, 1.0],
        "positions": [
            [0, 0, 0],
            [1, 0, 0],
            [2, 0.1, 0],
            [3, 0.4, 0.2],
        ],
        "debris": [
            [0.01, 0.0, 0.0],
            [0.02, 0.01, 0.0],
            [0.03, 0.02, 0.01],
        ],
        "gamma": [
            [500, 1.2],
            [511, 4.8],
            [520, 1.0],
        ],
    }

    score = classical_anomaly_score(test_data)
    print("Anomaly score:", score)
