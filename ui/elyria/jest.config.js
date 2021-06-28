module.exports = {
    "roots": [
        "<rootDir>/src"
    ],
    "transform": {
        "^.+\\.tsx?$": "ts-jest",
        ".+\\.(css|styl|less|sass|scss|png|svg|jpg|ttf|woff|woff2)$": "jest-transform-stub"
    },
    "globals": {
        'ts-jest': {
            "tsconfig": 'tsconfig.test.json'
        }
    },
    "testRegex": "(/__tests__/.*|(\\.|/)(test|spec))\\.tsx?$",
    "moduleFileExtensions": [
        "ts",
        "tsx",
        "js",
        "jsx",
        "json",
        "node"
    ],
    "setupFilesAfterEnv": ["<rootDir>/src/setupTests.ts"],
};
