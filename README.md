# YouTube Agno Workflow

A comprehensive research automation system powered by specialized AI agents for multi-source data collection and analysis.

## 🚀 Features

- **Multi-Agent Research Orchestration**: Coordinated team of specialized AI agents
- **YouTube Transcript Analysis**: Automated video content processing and insights
- **Academic Paper Research**: Scholarly article discovery and analysis via ArXiv
- **News and Community Monitoring**: Real-time current events tracking
- **Web Scraping and Synthesis**: Comprehensive web data collection
- **Real-time Data Verification**: Cross-referencing and fact-checking capabilities
- **FastAPI Web Server**: Modern, fast web API with automatic documentation
- **MongoDB Integration**: Scalable database for research data storage
- **Rate Limiting**: Built-in protection against API abuse

## 🏗️ Architecture

The system is built on a modular architecture with the following components:

### Core Components
- **FastAPI Web Server**: Handles HTTP requests and API endpoints
- **MongoDB Database**: Stores research sessions, agent data, and results
- **Google Gemini AI Models**: Powers the intelligent agents
- **Rate Limiting Middleware**: Protects against excessive requests

### Research Agents
- **YouTube Agent** (`agents/youtube_agent.py`): Video transcript analysis and content insights
- **Academic Agent** (`agents/academic_agent.py`): Research paper processing and academic literature review
- **News Agent** (`agents/news_agent.py`): Current events monitoring and news analysis
- **Web Agent** (`agents/web_agent.py`): General web scraping and data collection
- **Community Agent** (`agents/community_agent.py`): Social media insights and community monitoring
- **Verification Agent** (`agents/verification_agent.py`): Data validation and cross-referencing
- **Strategy Agent** (`agents/strategy_agent.py`): Research planning and task coordination
- **Synthesis Agent** (`agents/synthesis_agent.py`): Report generation and data synthesis

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local or remote instance)
- Google API Key (for Gemini models)
- Docker (optional, for MongoDB)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/richard-devbot/youtube-agno.git
   cd youtube-agno
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Configure your `.env` file**
   ```env
   # Google API Key for Gemini model
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Server configuration
   AGNO_URL=http://localhost:7777
   
   # Database configuration
   DB_URL=mongodb://mongoadmin:secret@localhost:27017
   DB_FILE=research_team.db
   ```

## 🚀 Quick Start

### Option 1: Web Interface
```bash
python research_team_ui.py
```
Navigate to `http://localhost:7777` to access the web interface.

### Option 2: API Server
```bash
python routes.py
```
API documentation available at `http://localhost:7777/docs`

### Option 3: Direct Agent Testing
```bash
python agno_test.py
```

## 📡 API Endpoints

The system provides RESTful API endpoints for interacting with the research agents:

- `GET /` - Health check and system status
- `POST /research` - Submit research requests to agent teams
- `GET /research/{session_id}` - Retrieve research session results
- `POST /agents/{agent_type}` - Direct agent interaction
- `GET /agents/status` - Agent availability and status

Full API documentation is available at `/docs` when running the server.

## 🗄️ Database Setup

### Using Docker (Recommended)
```bash
# Start MongoDB container
docker run -d \
  --name local-mongo \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo:latest

# Verify container is running
docker ps

# Connect to MongoDB shell (optional)
docker exec -it local-mongo mongosh
```

### Manual MongoDB Setup
1. Install MongoDB locally
2. Configure authentication
3. Update connection string in `.env`

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run individual agent tests:
```bash
python agno_test.py
```

## 📁 Project Structure

```
youtube-agno-workflow/
├── agents/                 # AI research agents
│   ├── __init__.py
│   ├── youtube_agent.py    # YouTube transcript analysis
│   ├── academic_agent.py   # Academic paper research
│   ├── news_agent.py       # News monitoring
│   ├── web_agent.py        # Web scraping
│   ├── community_agent.py  # Community insights
│   ├── verification_agent.py # Data verification
│   ├── strategy_agent.py   # Research planning
│   └── synthesis_agent.py  # Report synthesis
├── middleware/             # Server middleware
│   ├── __init__.py
│   └── rate_limit.py       # Rate limiting
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── config.py             # Shared configuration
├── requirements.txt      # Python dependencies
├── research_team.py      # Core team logic
├── research_team_ui.py   # Web interface
├── routes.py             # API routes
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Google Gemini API key (required)
- `AGNO_URL`: Server URL (default: http://localhost:7777)
- `DB_URL`: MongoDB connection string
- `DB_FILE`: SQLite database file (fallback)

### Agent Configuration
Each agent can be configured in `config.py`:
- Model selection (Gemini variants)
- Tool availability
- Rate limiting parameters
- Database connections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the `/docs` endpoint when running the server
- **Community**: Join our discussions in GitHub Discussions

## 🔮 Roadmap

- [ ] Enhanced agent coordination algorithms
- [ ] Real-time WebSocket updates
- [ ] Advanced caching mechanisms
- [ ] Multi-language support
- [ ] Plugin architecture for custom agents
- [ ] Integration with more data sources
- [ ] Advanced analytics and reporting
- [ ] Mobile-responsive web interface

---

**Built with ❤️ using Agno AI Framework**