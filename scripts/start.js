const { execSync } = require('child_process');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');

try {
    console.log('Installing Python dependencies with Python 3.12...');
    try {
        console.log('Installing specific dependencies...');
        execSync('py -3.12 -m pip install lark-oapi>=1.2.0 python-dotenv>=1.0.0 -i https://pypi.org/simple', { cwd: projectRoot, stdio: 'inherit' });
        execSync('py -3.12 -m pip install -r requirements.txt -i https://pypi.org/simple', { cwd: projectRoot, stdio: 'inherit' });
    } catch (installError) {
        console.warn('Warning: pip install failed. Attempting to start server anyway...');
    }
    
    console.log('Starting FastAPI server...');
    execSync('py -3.12 -m uvicorn main:app --host 0.0.0.0 --port 8000', { cwd: projectRoot, stdio: 'inherit' });
} catch (error) {
    console.error('Failed to start server:', error.message);
    process.exit(1);
}

