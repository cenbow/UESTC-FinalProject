#pragma once
#include <string>
#include <ctime>
class Logger
{
public:
	enum class Level {
		DEBUG = 100,
		INFO = 200,
		WARNING = 500,
		ERROR = 1000
	};
	
	Logger(string filepath, Level level) 
	{
		log_file = ofstream(filepath);
		level_ = level;
		fmt_ = "{time} {level}: {msg}\n";
	}
	
	void logging(Level level, string msg)
	{
		if (level < level_) return;
		/*
		// TODO:
		int i = fmt.find("{time}");
		fmt.replace(i, i + str("{time}").length(), string(time(nullptr));

		i = fmt.find("{level}");
		fmt.replace(i, i + str("{level}".length(), )*/

		log_file << msg << endl;
		log_file.flush();
	}
	void debug(string msg)
	{
		logging(Level::DEBUG, msg);
	}
	~Logger()
	{
		log_file.close();
	}
private:
	ofstream log_file;
	Level level_ = Level::DEBUG;
	string fmt_;
};