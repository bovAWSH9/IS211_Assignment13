

create TABLE IF NOT EXISTS students (
                                        id integer PRIMARY KEY,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL

                                    );


create TABLE IF NOT EXISTS quizzes (
                                    id integer PRIMARY KEY,
                                    subject text NOT NULL,
                                    number_of_questions integer NOT NULL,
                                    date text NOT NULL
                                );

create TABLE IF NOT EXISTS quizzes_result (
                                    quiz_id integer NOT NULL,
                                    student_id integer NOT NULL,
                                    score integer NOT NULL
                                );