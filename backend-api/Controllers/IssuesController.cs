using Microsoft.AspNetCore.Mvc;
using backend_api.Data;
using backend_api.Models;

namespace backend_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class IssuesController : ControllerBase
{
    private readonly AppDbContext _db;

    public IssuesController(AppDbContext db) => _db = db;

    [HttpPost]
    public async Task<ActionResult<Issue>> Create(Issue issue)
    {
        _db.Issues.Add(issue);
        await _db.SaveChangesAsync();
        return CreatedAtAction(nameof(Create), new { id = issue.Id }, issue);
    }
}