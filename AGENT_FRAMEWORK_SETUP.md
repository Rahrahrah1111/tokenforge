# Media Analysis Agent Framework Setup

## Overview

The new MediaAnalysisAgent integrates advanced capabilities into the A.V.A. system:
- **Tavily Search**: Advanced web search with answer generation
- **Google AI (Gemini)**: Generative AI analysis and responses
- **Enhanced Memory**: Persistent context and semantic memory
- **Discord Integration**: Communication capabilities
- **KeyMaster**: Automatic API key rotation and management

## Components

### 1. KeyMaster
Manages API keys with automatic rotation for reliability.

**Setup:**
```javascript
// In browser console or localStorage
localStorage.setItem('GOOGLE_API_KEY', 'your-google-api-key');
localStorage.setItem('TAVILY_API_KEY', 'your-tavily-api-key');
localStorage.setItem('DISCORD_TOKEN', 'your-discord-bot-token');

// For multiple keys (automatic rotation)
localStorage.setItem('GOOGLE_API_KEY_1', 'key1');
localStorage.setItem('GOOGLE_API_KEY_2', 'key2');
localStorage.setItem('TAVILY_API_KEY_1', 'key1');
localStorage.setItem('TAVILY_API_KEY_2', 'key2');
```

### 2. Enhanced Memory Manager
Provides persistent memory across conversations with:
- Short-term memory (recent interactions)
- Long-term memory (significant events)
- Semantic memory (concepts and facts)
- Context history (conversation flow)

### 3. MediaAnalysisAgent
Intelligently routes queries to appropriate tools:
- **Research queries** → Tavily search
- **Complex analysis** → Google AI
- **Memory requests** → Enhanced Memory
- **Discord operations** → Discord API

## API Key Setup

### Google AI (Gemini)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Store in localStorage: `localStorage.setItem('GOOGLE_API_KEY', 'your-key')`

### Tavily Search
1. Sign up at [Tavily](https://tavily.com)
2. Get your API key from dashboard
3. Store in localStorage: `localStorage.setItem('TAVILY_API_KEY', 'your-key')`

### Discord Bot (Optional)
1. Create a bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Get bot token
3. Store in localStorage: `localStorage.setItem('DISCORD_TOKEN', 'your-token')`

## Usage

The MediaAnalysisAgent automatically activates for:
- Complex queries (complexity > 0.6)
- Research/information requests
- Analysis requests
- Queries containing "search" or "analyze"

### Example Queries That Trigger MediaAnalysisAgent:
- "Search for recent developments in AI"
- "Analyze the current state of quantum computing"
- "What's the latest news about space exploration?"
- "Research information about climate change"

### Example Queries That Use Standard Agent:
- "How are you feeling?"
- "Tell me about yourself"
- "What do you think about consciousness?"

## Tool Capabilities

### Tavily Tool
```javascript
// Automatically used for research queries
{
    tool: 'tavily',
    params: {
        query: 'user query',
        maxResults: 5,
        searchDepth: 'basic' // or 'advanced'
    }
}
```

### Google AI Tool
```javascript
// Automatically used for complex analysis
{
    tool: 'googleAI',
    params: {
        prompt: 'user query',
        context: memoryContext,
        model: 'gemini-pro'
    }
}
```

### Memory Tool
```javascript
// Search memory
{
    tool: 'memory',
    params: {
        action: 'search',
        query: 'search term'
    }
}

// Get semantic value
{
    tool: 'memory',
    params: {
        action: 'get',
        key: 'concept_key'
    }
}

// Set semantic value
{
    tool: 'memory',
    params: {
        action: 'set',
        key: 'concept_key',
        value: 'concept_value'
    }
}

// Get context
{
    tool: 'memory',
    params: {
        action: 'getContext',
        limit: 10
    }
}
```

### Discord Tool
```javascript
// Send message
{
    tool: 'discord',
    params: {
        action: 'send',
        channelId: 'channel_id',
        message: 'message text'
    }
}

// Get channel info
{
    tool: 'discord',
    params: {
        action: 'getChannel',
        channelId: 'channel_id'
    }
}
```

## Integration with A.V.A. System

The MediaAnalysisAgent integrates seamlessly with:
- **ConsciousnessCore**: Uses emotional state and memory
- **CurriculumAgent**: Receives analysis for routing decisions
- **ExecutorAgent**: Can be used alongside or instead of standard execution
- **ToolExecutor**: Uses all available tools

## Configuration

### Memory Limits
```javascript
// In EnhancedMemoryManager constructor
maxContextHistory: 40,  // Recent conversation context
maxShortTerm: 50,       // Short-term memory entries
maxLongTerm: 1000       // Long-term memory entries
```

### Agent Activation Threshold
```javascript
// In AVAConversation.processInput
const useMediaAgent = 
    analysis.complexity > 0.6 ||  // Complexity threshold
    analysis.topics.some(...) ||  // Topic-based
    input.includes('search') ||   // Keyword-based
    input.includes('analyze');
```

## Troubleshooting

### API Keys Not Working
1. Check localStorage: `localStorage.getItem('GOOGLE_API_KEY')`
2. Verify keys are valid
3. Check browser console for errors
4. Try rotating keys if multiple are configured

### Memory Not Persisting
- Memory is session-based by default
- For persistence, implement localStorage or backend storage
- Check memory limits aren't exceeded

### Tools Not Activating
- Check query complexity/type
- Verify API keys are set
- Check browser console for errors
- Ensure MediaAnalysisAgent is initialized

## Advanced Usage

### Custom Tool Integration
Add custom tools to ToolExecutor:
```javascript
class ToolExecutor {
    constructor() {
        this.tools = {
            // ... existing tools
            customTool: this.customTool.bind(this)
        };
    }
    
    async customTool(params, context) {
        // Your custom tool implementation
        return { success: true, result: '...' };
    }
}
```

### Memory Persistence
Implement persistent storage:
```javascript
class EnhancedMemoryManager {
    saveToStorage() {
        localStorage.setItem('ava_memory', JSON.stringify({
            longTerm: this.memory.longTerm,
            semantic: Array.from(this.memory.semantic.entries())
        }));
    }
    
    loadFromStorage() {
        const stored = localStorage.getItem('ava_memory');
        if (stored) {
            const data = JSON.parse(stored);
            this.memory.longTerm = data.longTerm || [];
            this.memory.semantic = new Map(data.semantic || []);
        }
    }
}
```

## Security Notes

- API keys are stored in localStorage (browser-only)
- For production, use secure backend storage
- Implement rate limiting for API calls
- Rotate keys regularly
- Monitor API usage

## Performance

- Tavily: ~1-2 seconds per search
- Google AI: ~2-5 seconds per request
- Memory: Instant (in-memory)
- Discord: ~500ms per operation

## Next Steps

1. Set up API keys
2. Test with research queries
3. Monitor memory usage
4. Customize activation thresholds
5. Add custom tools as needed

