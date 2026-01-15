using Microsoft.AspNetCore.Mvc;
using backend_api.Data;
using backend_api.Models;

namespace backend_api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UsersController : ControllerBase
{
    private readonly AppDbContext _db;

    public UsersController(AppDbContext db) => _db = db;

    [HttpPost]
    public async Task<ActionResult<User>> Create(User user)
    {
        user.CreatedAt = DateTime.UtcNow;
        _db.Users.Add(user);
        await _db.SaveChangesAsync();
        return CreatedAtAction(nameof(Create), new { id = user.Id }, user);
    }
}