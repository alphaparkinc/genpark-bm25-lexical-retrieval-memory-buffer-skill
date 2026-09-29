import sys
import json
from client import BM25MemoryBuffer

bm = BM25MemoryBuffer()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-bm25-lexical-retrieval-memory-buffer-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "index_bm25_memory",
                        "description": "Add new document entry to BM25 inverted index",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "doc_id": {"type": "string"},
                                "text": {"type": "string"}
                            },
                            "required": ["doc_id", "text"]
                        }
                    },
                    {
                        "name": "query_bm25_memory",
                        "description": "Search indexed memory using BM25 Okapi ranking",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"},
                                "top_k": {"type": "integer", "default": 3}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "index_bm25_memory":
            bm.add_document(args.get("doc_id"), args.get("text"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Document indexed"}]}}
        elif tool_name == "query_bm25_memory":
            q = args.get("query", "")
            k = args.get("top_k", 3)
            hits = bm.search(q, k)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(hits)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
