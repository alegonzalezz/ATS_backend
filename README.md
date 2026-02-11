# Python Backend with Vercel and Supabase

A serverless Python backend API built with Flask, deployed on Vercel, and using Supabase as the database.

## Features

- ✅ RESTful API with CRUD operations
- ✅ Serverless deployment on Vercel
- ✅ Supabase database integration
- ✅ CORS enabled for cross-origin requests
- ✅ Generic endpoints for any table
- ✅ Error handling and validation
- ✅ Environment-based configuration

## Project Structure

```
ATS_backend/
├── api/
│   ├── index.py          # Main Flask application
│   └── database.py       # Supabase client and database utilities
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment configuration
└── README.md            # This file
```

## Prerequisites

- Python 3.9 or higher
- A Supabase account and project ([supabase.com](https://supabase.com))
- Vercel account for deployment ([vercel.com](https://vercel.com))

## Local Development Setup

### 1. Clone and Navigate to Project

```bash
cd /Volumes/SSD/Mac/workplace/ATS_backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and add your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
FLASK_ENV=development
```

**Where to find your Supabase credentials:**
1. Go to your Supabase project dashboard
2. Click on "Settings" → "API"
3. Copy the "Project URL" (SUPABASE_URL)
4. Copy the "anon public" key (SUPABASE_KEY)

### 5. Run the Development Server

```bash
python api/index.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check

```bash
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "message": "API is running successfully"
}
```

### Get All Records

```bash
GET /api/<table_name>
```

Optional query parameters for filtering:
```bash
GET /api/users?status=active&role=admin
```

### Get Single Record

```bash
GET /api/<table_name>/<record_id>
```

### Create Record

```bash
POST /api/<table_name>
Content-Type: application/json

{
  "field1": "value1",
  "field2": "value2"
}
```

### Update Record

```bash
PUT /api/<table_name>/<record_id>
Content-Type: application/json

{
  "field1": "new_value"
}
```

### Delete Record

```bash
DELETE /api/<table_name>/<record_id>
```

## Example Usage

### Create a table in Supabase

1. Go to your Supabase dashboard
2. Navigate to "Table Editor"
3. Create a new table (e.g., "tasks")
4. Add columns as needed

### Test the API

```bash
# Get all tasks
curl http://localhost:5000/api/tasks

# Create a new task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My first task", "status": "pending"}'

# Update a task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'

# Delete a task
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Deployment to Vercel

### Option 1: Using Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel
```

4. Add environment variables in Vercel dashboard:
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Add `SUPABASE_URL` and `SUPABASE_KEY`

5. Redeploy to apply environment variables:
```bash
vercel --prod
```

### Option 2: Using Vercel Dashboard

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
6. Click "Deploy"

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Your Supabase project URL | Yes |
| `SUPABASE_KEY` | Your Supabase anon/public key | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message here"
}
```

HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

## Security Notes

- Never commit `.env` file to version control
- Use environment variables for sensitive data
- The `SUPABASE_KEY` should be the anon/public key, not the service role key
- Implement Row Level Security (RLS) in Supabase for production
- Consider adding authentication middleware for protected endpoints

## Next Steps

1. **Add Authentication**: Integrate Supabase Auth for user authentication
2. **Add Validation**: Implement request validation using libraries like `marshmallow`
3. **Add Tests**: Write unit and integration tests
4. **Add Rate Limiting**: Implement rate limiting for API endpoints
5. **Add Logging**: Set up proper logging for debugging and monitoring
6. **Custom Endpoints**: Create specific endpoints for your business logic

## Troubleshooting

### "SUPABASE_URL and SUPABASE_KEY must be set"
- Make sure your `.env` file exists and contains the correct values
- For Vercel deployment, ensure environment variables are set in the dashboard

### "Table does not exist"
- Verify the table name matches exactly (case-sensitive)
- Check that the table exists in your Supabase project

### CORS errors
- CORS is enabled by default for all origins
- Modify `CORS(app)` in `api/index.py` to restrict origins if needed

## License

MIT
