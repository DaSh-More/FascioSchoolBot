CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    role TEXT NOT NULL,
    state TEXT NOT NULL
);

CREATE TABLE Courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    describe TEXT
);

CREATE TABLE Events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    date DATE,
    FOREIGN KEY (course_id) REFERENCES Courses(id)
);

CREATE TABLE UserOnGroup (
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (group_id) REFERENCES Events(id)
);

CREATE TABLE UserOnEvent (
    user_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (event_id) REFERENCES Events(id)
)
